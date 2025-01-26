from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import logging
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--lang=en')
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def scrape_google_maps(area, max_results=20, retries=3):
    driver = setup_chrome_driver()
    police_stations = []
    wait = WebDriverWait(driver, 10)
    
    try:
        search_query = f"police station in {area}, Sri Lanka"
        url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
        logger.info(f"Searching for police stations in {area}")
        
        for attempt in range(retries):
            try:
                driver.get(url)
                
                # Wait for results to load
                results = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.Nv2PK")))
                
                for result in results[:max_results]:
                    try:
                        name = wait.until(EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "h3.fontHeadlineSmall"))).text
                        address = result.find_element(By.CSS_SELECTOR, 
                            "div.W4Efsd:nth-child(2)").text.split("·")[0].strip()
                        
                        station = {
                            'name': name,
                            'address': address,
                            'area': area
                        }
                        police_stations.append(station)
                        logger.info(f"Found station: {name}")
                    except Exception as e:
                        logger.error(f"Error extracting station details: {str(e)}")
                
                break
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == retries - 1:
                    logger.error(f"Failed to scrape {area} after {retries} attempts")
                time.sleep(2)
    finally:
        driver.quit()
    
    return police_stations

def main():
    areas = ["Arugam Bay", "Nuwara Eliya", "Kandy"]
    all_stations = []
    
    for area in areas:
        logger.info(f"Scraping police stations in {area}...")
        stations = scrape_google_maps(area)
        all_stations.extend(stations)
        logger.info(f"Found {len(stations)} police stations in {area}")
        time.sleep(3)  # Delay between areas
    
    if all_stations:
        df = pd.DataFrame(all_stations)
        df.to_csv('police_stations.csv', index=False)
        logger.info(f"Saved {len(all_stations)} police stations to police_stations.csv")
    else:
        logger.warning("No police stations found")

if __name__ == "__main__":
    main()