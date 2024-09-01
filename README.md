NumberDB

Welcome to NumberDB—an advanced scraping tool designed to extract and manage business listings from Yellow Pages and Yelp. Leveraging the power of Python, this project allows you to efficiently scrape and store vast amounts of business data into an SQLite database, ensuring no duplicate entries while maintaining a seamless scraping experience.
🚀 Features

    Multi-Platform Scraping: Seamlessly scrape data from both Yellow Pages and Yelp.
    Database Management: Automatically detect and prevent duplicate entries, ensuring your database stays clean and organized.
    Error Handling & Logging: Comprehensive error handling and logging to monitor scraping progress and any potential issues.
    Resume Scraping: Save and resume scraping progress, allowing you to pause and continue without losing any data.
    Scalable Performance: Capable of handling large-scale scraping operations, with optimized rate limiting and user-agent rotation.

📂 Project Structure

plaintext

numberdb/
├── .gitignore
├── errors.py          # Custom error handling
├── main.py            # Entry point for running the scraper
├── requirements.txt   # Dependencies for the project
├── utils.py           # Utility functions, including user-agent rotation
├── yelp.db            # SQLite database for Yelp scraping
├── yelp.py            # Yelp-specific scraping logic
├── yelp_db.py         # Database management for Yelp scraping
├── yp.py              # Yellow Pages-specific scraping logic
├── yp_db.py           # Database management for Yellow Pages scraping
└── yp_scraper.py      # Core Yellow Pages scraping functions

🛠️ Getting Started
Prerequisites

    Python 3.9+
    SQLite

Installation

    Clone the repository:

    bash

git clone https://github.com/havokzero/numberdb.git
cd numberdb

Install dependencies:

bash

    pip install -r requirements.txt

Running the Scraper

To start scraping, simply run the main.py script:

bash

python main.py

You'll be prompted to choose between Yellow Pages and Yelp for scraping. The scraper will then begin fetching and storing business listings in the respective SQLite database.
📊 Performance

    Speed: The scraper is capable of pulling approximately 45,000 entries per hour.
    Scalability: Designed to handle large datasets, capable of scaling to scrape millions of records over time.

📝 License

This project is licensed under the MIT License—see the LICENSE file for details.
👤 Author

    havokzero - GitHub Profile
