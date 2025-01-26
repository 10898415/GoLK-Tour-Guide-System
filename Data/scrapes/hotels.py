from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import pyshorteners  # For shortening URLs

def setup_driver():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--headless')  # Run in headless mode for efficiency
    service = Service()
    return webdriver.Chrome(service=service, options=options)

def shorten_url(url):
    """Shorten a URL using pyshorteners."""
    try:
        shortener = pyshorteners.Shortener()
        return shortener.tinyurl.short(url)  # Use TinyURL to shorten the link
    except Exception as e:
        print(f"Error shortening URL: {e}")
        return url  # Return the original URL if shortening fails

def scrape_google_maps(location, max_hotels=10):
    driver = setup_driver()
    wait = WebDriverWait(driver, 20)
    hotels = []
    unique_hotels = set()  # To avoid duplicates

    try:
        # Navigate to Google Maps
        driver.get("https://www.google.com/maps")

        # Find and fill search box
        search_box = wait.until(EC.presence_of_element_located(
            (By.ID, "searchboxinput")))
        search_box.send_keys(f"hotels in {location}")
        search_box.send_keys(Keys.ENTER)

        # Wait for results to load
        time.sleep(5)

        # Scroll to load more results
        scrollable_div = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f'[aria-label*="Results for hotels in {location}"]')))

        # Keep scrolling until we have enough unique hotels
        while len(unique_hotels) < max_hotels:
            # Scroll down
            driver.execute_script(
                'arguments[0].scrollTop = arguments[0].scrollHeight',
                scrollable_div)
            time.sleep(2)  # Wait for new results to load

            # Extract hotel elements
            hotel_elements = driver.find_elements(
                By.CSS_SELECTOR,
                'div[jsaction*="mouseover:pane"]'
            )

            for element in hotel_elements:
                try:
                    name = element.find_element(
                        By.CSS_SELECTOR,
                        'div.fontHeadlineSmall'
                    ).text

                    # Skip if the hotel is already in the set
                    if name in unique_hotels:
                        continue

                    try:
                        rating = element.find_element(
                            By.CSS_SELECTOR,
                            'span.fontBodyMedium > span'
                        ).text
                    except:
                        rating = "N/A"

                    try:
                        link = element.find_element(
                            By.CSS_SELECTOR,
                            'a'
                        ).get_attribute('href')
                        # Shorten the Google Map link
                        short_link = shorten_url(link)
                    except:
                        short_link = "N/A"

                    # Add hotel to the list
                    hotels.append({
                        'area': location,
                        'hotel': name,
                        'ratings': rating,
                        'google_map_link': short_link
                    })
                    unique_hotels.add(name)  # Add to set to track uniqueness

                    # Stop if we have enough hotels
                    if len(unique_hotels) >= max_hotels:
                        break

                except Exception as e:
                    print(f"Error extracting hotel details: {e}")
                    continue

    except Exception as e:
        print(f"Error scraping {location}: {e}")
    finally:
        driver.quit()

    return hotels

def scrape_multiple_areas(areas, max_hotels=10):
    all_hotels = []
    for area in areas:
        print(f"Scraping hotels in {area}...")
        hotels = scrape_google_maps(area, max_hotels)
        all_hotels.extend(hotels)
        print(f"Found {len(hotels)} hotels in {area}.")

    # Save all results to a single CSV file
    df = pd.DataFrame(all_hotels)
    df.to_csv('all_hotels.csv', index=False)
    print(f"Saved {len(all_hotels)} hotels to all_hotels.csv")

if __name__ == "__main__":
    # List of areas to scrape (in the specified order)
    areas = [
        "Arugam Bay",
        "Nuwara Eliya",
        "Kandy",
        "Kataragama",
        "Anuradhapura",
        "Polonnaruwa",
        "Sigiriya",
        "Trincomalee",
        "Jaffna",
        "Kalpitiya",
        "Passikudah",
        "Bentota",
        "Haputale",
        "Matara",
        "Puttalam",
        "Weligama",
        "Badulla",
        "Hambantota",
        "Diyatalawa",
        "Negombo",
        "Ella",
        "Hikkaduwa",
        "Galle",
        "Bandarawela",
        "Ratnapura",
        "Knuckles",
        "Kitulgala",
        "Tangalle",
        "Maskeliya",
        "Mannar",
        "Mirissa",
        "Pottuvil",
        "Mullaitivu",
        "Dambulla",
        "Avissawella",
        "Kalutara",
        "Deniyaya",
        "Monaragala",
        "Tissamaharama",
        "Sella Kataragama",
        "Colombo",
        "Gampaha",
        "Dodanduwa",
        "Horton Plains",
        "Sinharaja",
        "Chilaw",
        "Matale",
        "Kurunegala",
        "Ambalangoda"
    ]

    # Scrape hotels for all areas
    scrape_multiple_areas(areas, max_hotels=10)