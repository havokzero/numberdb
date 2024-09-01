import requests
import logging
import os
import time
from tqdm import tqdm
import random

class YelpAPI:
    def __init__(self):
        self.api_key = os.getenv('YELP_API_KEY')
        self.base_url = 'https://api.yelp.com/v3/businesses'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        self.max_retries = 5

    def search_business(self, term, location, offset=0, limit=50):
        search_url = f'{self.base_url}/search'
        params = {
            'term': term,
            'location': location,
            'limit': limit,
            'offset': offset
        }

        for attempt in range(self.max_retries):
            response = requests.get(search_url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                delay = 60 * (2 ** attempt) + random.uniform(0.10)  # Expontential Backoff with jitter
                logging.error(f"Rate limit reached. Retrying in {delay:.2f} seconds... (Attempt {attempt + 1}/{self.max_retries})")
                time.sleep(delay)  # changed  Wait for 60 delay to delay for exponential backoff
            else:
                logging.error(f"Yelp API request failed: {response.status_code} - {response.text}")
                return None

        logging.error("Max retries reached. Failed to retrieve data from Yelp API.")
        return None

    def get_business_details(self, business_id):
        details_url = f'{self.base_url}/{business_id}'
        response = requests.get(details_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Yelp API request for business details failed: {response.status_code} - {response.text}")
            return None

    def get_business_reviews(self, business_id):
        reviews_url = f'{self.base_url}/{business_id}/reviews'
        response = requests.get(reviews_url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"Yelp API request for business reviews failed: {response.status_code} - {response.text}")
            return None

    def scrape_yelp(self, term, location, db_manager):
        offset = db_manager.get_last_offset(term, location)  # Get the last offset from the database
        total_businesses = 0
        while offset + 50 <= 240:  # Ensure that limit + offset <= 240
            data = self.search_business(term, location, offset=offset)
            if not data or not data.get('businesses'):
                break

            businesses = data['businesses']
            for business in tqdm(businesses, desc="Processing Yelp Results"):
                if not db_manager.entry_exists(business):
                    db_manager.save_to_database(business)
                    total_businesses += 1

            logging.info(f"Scraped {len(businesses)} Yelp listings from offset {offset}")
            offset += len(businesses)
            db_manager.save_progress(term, location, offset)  # Save progress

        logging.info(f"Scraping Yelp complete. {total_businesses} new listings saved to the database.")
