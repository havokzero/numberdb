import logging
import concurrent.futures
from yp import YellowPagesScraper
from yelp import YelpAPI
from yp_db import YPDatabaseManager
from yelp_db import YelpDatabaseManager
from utils import load_environment_variables
from termcolor import colored
from colorama import init  # Add this import

# Initialize colorama
init(autoreset=True)

# List of state codes in the United States to scrape
US_STATE_CODES = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
    'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT',
    'VA', 'WA', 'WV', 'WI', 'WY'
]

def scrape_yellow_pages(state_code, yp_db):
    logging.info(colored(f"Starting Yellow Pages scraping for {state_code}...", "blue"))
    yp_scraper = YellowPagesScraper(state_code)  # You can pass a specific search term here if needed
    yp_scraper.scrape_yellow_pages(db_manager=yp_db)
    logging.info(colored(f"Finished scraping for {state_code}.", "green"))


def scrape_yelp(locations, yelp_db):
    logging.info(colored("Starting Yelp API scraping...", "blue"))
    yelp_api = YelpAPI()
    for location in locations:
        yelp_api.scrape_yelp('', location, db_manager=yelp_db)
    logging.info(colored(f"Total Yelp entries in the database: {yelp_db.get_total_entries()}", "green"))

def main():
    load_environment_variables()

    # Prompt user for input to choose which platform to scrape
    print(colored("Choose a platform to scrape:", "yellow"))
    print(colored("1. Yellow Pages", "cyan"))
    print(colored("2. Yelp", "cyan"))
    choice = input(colored("Enter your choice (1 or 2): ", "yellow"))

    if choice == '1':
        # Initialize Yellow Pages database manager
        yp_db = YPDatabaseManager('yellowpages.db')
        yp_db.setup_database()

        # Use ThreadPoolExecutor to scrape multiple states concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(scrape_yellow_pages, state_code, yp_db) for state_code in US_STATE_CODES]

            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()  # We can also process the result here if needed
                except Exception as e:
                    logging.error(f"An error occurred: {e}")

    elif choice == '2':
        # Initialize Yelp database manager
        yelp_db = YelpDatabaseManager('yelp.db')
        yelp_db.setup_database()

        # Scraping across all US states
        locations = [state for state in US_STATE_CODES]

        # Start scraping Yelp
        scrape_yelp(locations, yelp_db)

    else:
        print(colored("Invalid choice. Please enter 1 or 2.", "red"))
        return

    logging.info(colored("Process completed successfully.", "blue"))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        main()
    except KeyboardInterrupt:
        print(colored("\nProcess Interrupted by Havok. Exiting Program....", "red"))
