import requests
import xml.etree.ElementTree as ET
import gzip
import shutil
import os
import threading
import asyncio
from playwright.async_api import async_playwright
import json
import logging
from tqdm.asyncio import tqdm


def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config["headers"], config["cookies"]


def save_cookies(cookies):
    """Save cookies to config file"""
    with open("config.json", "r") as f:
        config = json.load(f)
    config["cookies"].update(cookies)
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)


HEADERS, COOKIES = load_config()


# Replace existing logging configuration with:
def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # File handler - detailed logging
    file_handler = logging.FileHandler("scraper.log")
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_format)

    # Console handler - less detailed, more visual
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_format)

    # Add both handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


logger = setup_logging()


async def setup_browser():
    """
    Setup and return a headless Playwright browser instance
    """
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True,
        args=[
            "--disable-dev-shm-usage",
            "--no-sandbox",
            "--disable-setuid-sandbox",
        ],
    )
    context = await browser.new_context()

    # Set cookies
    for name, value in COOKIES.items():
        await context.add_cookies(
            [{"name": name, "value": value, "url": "https://www.booking.com"}]
        )

    return browser, playwright, context


class SitemapReader:
    def __init__(self, url):
        self.url = url
        self.urls = []
        self.browser = None
        self.playwright = None

    async def fetch_sitemap(self):
        logger.info(f"Fetching sitemap from {self.url}")
        try:
            self.browser, self.playwright, self.context = await setup_browser()
            page = await self.context.new_page()
            await page.set_extra_http_headers(HEADERS)
            response = await page.goto(self.url, wait_until="networkidle")

            # Capture and save new cookies
            cookies = await self.context.cookies()
            new_cookies = {cookie["name"]: cookie["value"] for cookie in cookies}
            save_cookies(new_cookies)

            # Get raw response content instead of rendered HTML
            self.sitemap_content = await response.body()

            # Try to decode the content - it might be gzipped
            try:
                self.sitemap_content = gzip.decompress(self.sitemap_content)
            except:
                pass  # If not gzipped, use as is

            # Ensure we have string content for XML parsing
            if isinstance(self.sitemap_content, bytes):
                self.sitemap_content = self.sitemap_content.decode("utf-8")

            # Validate response
            if not response.ok:
                raise Exception(f"Failed to fetch sitemap: HTTP {response.status}")

            # Validate content type
            content_type = response.headers.get("content-type", "")
            if not any(
                t in content_type.lower()
                for t in ["xml", "text/plain", "application/x-gzip"]
            ):
                logger.warning(f"Unexpected content type: {content_type}")

            # Validate content
            if not self.sitemap_content or len(self.sitemap_content) < 100:
                raise Exception("Sitemap content appears to be empty or too short")

            if "<?xml" not in self.sitemap_content:
                logger.error("Content does not appear to be XML")
                logger.debug(f"Content preview: {self.sitemap_content[:500]}")
                raise Exception("Invalid sitemap format")

            logger.info("Successfully fetched sitemap")
            logger.debug(f"Content size: {len(self.sitemap_content)} bytes")

        except Exception as e:
            logger.error(f"Error fetching sitemap: {e}")
            raise
        finally:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()

    def parse_sitemap(self):
        logger.info("Parsing sitemap XML")
        try:
            # Clean up the content before parsing
            self.sitemap_content = self.sitemap_content.strip()
            with open("sitemap.xml", "w", encoding="utf-8") as f:
                f.write(self.sitemap_content)

            root = ET.fromstring(self.sitemap_content)
            # Find all loc elements directly
            for sitemap_link in root:
                if sitemap_link is not None and sitemap_link[0].text:
                    self.urls.append(sitemap_link[0].text)

            # Validate parsed content
            if not self.urls:
                raise Exception("No URLs found in sitemap")

            if not any("en_us" in url for url in self.urls):
                logger.warning("No English (US) URLs found in sitemap")

            logger.info(f"Found {len(self.urls)} URLs in sitemap")
            logger.debug(f"Sample URLs: {self.urls[:3]}")

        except ET.ParseError as e:
            logger.error(f"XML Parsing error: {e}")
            logger.debug(f"Content preview: {self.sitemap_content[:500]}")
            raise

    def get_urls(self):
        """
        Get the list of URLs extracted from the sitemap.
        """
        return self.urls


async def download_gz_file(url, output_dir):
    try:
        logger.debug(f"Downloading: {url}")
        browser, playwright, context = await setup_browser()
        page = await context.new_page()
        await page.set_extra_http_headers(HEADERS)

        # Set up download listener
        download_size = 0
        progress_bar = None

        async def handle_response(response):
            nonlocal download_size, progress_bar
            if response.url == url:
                content_length = int(response.headers.get("content-length", 0))
                if content_length:
                    download_size = content_length
                    progress_bar = tqdm(
                        total=content_length,
                        unit="B",
                        unit_scale=True,
                        desc=f"Downloading {url.split('/')[-1]}",
                        ncols=80,
                    )

        page.on("response", handle_response)
        response = await page.goto(url, wait_until="networkidle")

        # Get content with progress updates
        content = bytearray()
        async for chunk in response.body():
            content.extend(chunk)
            if progress_bar:
                progress_bar.update(len(chunk))

        if progress_bar:
            progress_bar.close()

        # Rest of the function remains the same
        filename = url.split("/")[-1]
        logger.debug(f"Saving to: {filename}")
        gz_path = os.path.join(output_dir, filename)

        with open(gz_path, "wb") as file:
            file.write(content)

        # Extract the .gz file
        extracted_path = gz_path.rstrip(".gz")
        with gzip.open(gz_path, "rb") as gz_file, open(
            extracted_path, "wb"
        ) as extracted_file:
            shutil.copyfileobj(gz_file, extracted_file)

        os.remove(gz_path)
        logger.debug(f"Successfully processed: {filename}")
        return extracted_path
    except Exception as e:
        logger.error(f"Error downloading {url}: {e}")
        raise
    finally:
        if "progress_bar" in locals() and progress_bar:
            progress_bar.close()
        await browser.close()
        await playwright.stop()


async def main():
    try:
        logger.info("=" * 50)
        logger.info("Starting new scraping session")

        sitemap_url = "https://www.booking.com/sitembk-hotel-index.xml"
        logger.info("Starting scraper")

        reader = SitemapReader(sitemap_url)
        await reader.fetch_sitemap()
        reader.parse_sitemap()
        urls = reader.get_urls()

        # Validate URLs
        if not urls:
            raise Exception("No URLs found in sitemap")

        output_directory = "./temp"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            logger.info(f"Created output directory: {output_directory}")

        zip_urls = [url for url in urls if "en-us" in url]
        if not zip_urls:
            raise Exception("No English (US) URLs found")

        logger.info(f"Found {len(zip_urls)} files to download")
        logger.debug(f"First 3 URLs: {zip_urls[:3]}")

        # Sequential downloads with delay
        results = []
        for i, url in enumerate(zip_urls):
            if i > 0:  # Don't delay before first download
                logger.info("Waiting 5 seconds before next download...")
                await asyncio.sleep(5)

            result = await download_gz_file(url, output_directory)
            results.append(result)

        logger.info("All files downloaded and extracted successfully")
        logger.info(f"Processed {len(results)} files")
        logger.debug(f"Processed files: {results}")

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
