import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# Function to scrape a single page
def scrape_page(url, session):
    # Add a random delay to avoid detection
    time.sleep(random.randint(2, 5))

    # Send a GET request to the URL
    response = session.get(url)
    print(f"Response Status Code: {response.status_code}")  # Debugging: Check if the request is successful

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    destinations = []

    # Find all tourist attraction elements on the page
    for item in soup.find_all('div', class_='attraction_element'):
        # Extract the name of the attraction
        name = item.find('div', class_='listing_title')
        # Extract the location of the attraction
        location = item.find('div', class_='address')
        # Extract the rating of the attraction
        rating = item.find('span', class_='ui_bubble_rating')

        # Ensure all required data is present
        if name and location:
            name = name.text.strip()
            location = location.text.strip()
            rating = rating['alt'] if rating else 'No rating'
            # Append the data to the destinations list
            destinations.append({"Name": name, "Location": location, "Rating": rating})
            print(f"Scraped: {name}, {location}, {rating}")  # Debugging: Print each scraped item

    return destinations

# Function to scrape multiple pages
def scrape_tripadvisor(base_url, num_pages):
    # Create a session object
    session = requests.Session()
    # Set headers to mimic a real browser
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": "https://www.tripadvisor.com/",
        "Upgrade-Insecure-Requests": "1",
    })

    all_destinations = []
    # Loop through multiple pages (TripAdvisor pagination increments by 30)
    for page in range(0, num_pages * 30, 30):
        url = f"{base_url}-oa{page}-Sri_Lanka.html"
        print(f"Scraping {url}...")
        destinations = scrape_page(url, session)
        all_destinations.extend(destinations)
    return all_destinations

# Base URL for TripAdvisor Sri Lanka attractions
base_url = "https://www.tripadvisor.com/Attractions-g293961-Activities"
num_pages = 5  # Number of pages to scrape (adjust as needed)

# Scrape data
print("Starting scraping process...")
destinations = scrape_tripadvisor(base_url, num_pages)

# Save to CSV
if destinations:
    df = pd.DataFrame(destinations)
    df.to_csv('sri_lanka_tourist_destinations.csv', index=False)
    print(f"Data saved to sri_lanka_tourist_destinations.csv with {len(df)} entries.")
else:
    print("No data scraped. Check the script and website structure.")