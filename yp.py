import requests
from bs4 import BeautifulSoup
import logging
import time
import random
import urllib.parse
from utils import get_random_user_agent

class YellowPagesScraper:
    def __init__(self, state_code, search_term='business'):
        self.state_code = state_code
        self.search_term = search_term if search_term else 'business'
        self.base_url = f'https://www.yellowpages.com/search?search_terms={urllib.parse.quote_plus(self.search_term)}&geo_location_terms={urllib.parse.quote_plus(self.state_code)}'
        self.headers = {
            'User-Agent': get_random_user_agent()
        }

    def fetch_page(self, url):
        try:
            time.sleep(random.uniform(0.1, 0.5))  # Short delay to avoid being blocked
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            return None
        except requests.RequestException as e:
            logging.error(f"Failed to fetch page: {e}")
            return None

    def parse_listing(self, listing):
        try:
            name = listing.find('a', class_='business-name').get_text(strip=True)
            phone = listing.find('div', class_='phones phone primary').get_text(strip=True)
            address = listing.find('div', class_='street-address').get_text(strip=True)
            locality = listing.find('div', class_='locality').get_text(strip=True)
            city, state_zip = locality.split(', ')
            state, zip_code = state_zip.split(' ')
            business_type = listing.find('div', class_='categories').get_text(strip=True)
            return {
                'name': name,
                'phone': phone,
                'address': address,
                'city': city,
                'state': state,
                'zip': zip_code,
                'type': business_type,
                'notes': ''
            }
        except AttributeError as e:
            logging.warning(f"Error parsing listing: {e}")
            return None

    def scrape_yellow_pages(self, db_manager=None):
        all_listings = []
        page = 1
        while True:
            search_url = f'{self.base_url}&page={page}'
            page_content = self.fetch_page(search_url)
            if not page_content:
                break

            soup = BeautifulSoup(page_content, 'html.parser')
            listings = soup.find_all('div', class_='result')

            if not listings:
                break  # No more pages

            for listing in listings:
                business_info = self.parse_listing(listing)
                if business_info and db_manager:
                    if not db_manager.entry_exists(business_info):
                        db_manager.save_to_database(business_info)
                        all_listings.append(business_info)

            logging.info(f"Scraped {len(listings)} listings from page {page}")
            page += 1  # Move to the next page

        logging.info(f"Scraping complete. {len(all_listings)} new listings saved to the database.")
        return len(all_listings)
