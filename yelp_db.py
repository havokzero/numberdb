import sqlite3
import logging

class YelpDatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def setup_database(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS yelp (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    business_id TEXT UNIQUE,
                    name TEXT,
                    phone TEXT,
                    address TEXT,
                    city TEXT,
                    state TEXT,
                    zip TEXT,
                    rating REAL,
                    review_count INTEGER,
                    price TEXT,
                    categories TEXT,
                    url TEXT,
                    image_url TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS yelp_progress (
                    id INTEGER PRIMARY KEY,
                    search_term TEXT,
                    location TEXT,
                    last_offset INTEGER
                )
            ''')
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logging.error(f"Failed to create database table: {e}")

    def entry_exists(self, business_info):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 1 FROM yelp WHERE business_id = :id
            ''', {'id': business_info.get('id', '')})
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except sqlite3.Error as e:
            logging.error(f"Failed to check if entry exists in the database: {e}")
            return False

    def save_to_database(self, business_info):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO yelp (business_id, name, phone, address, city, state, zip, rating, review_count, price, categories, url, image_url)
                VALUES (:id, :name, :phone, :address1, :city, :state, :zip_code, :rating, :review_count, :price, :categories, :url, :image_url)
            ''', {
                'id': business_info.get('id', ''),
                'name': business_info.get('name', ''),
                'phone': business_info.get('display_phone', ''),
                'address1': business_info.get('location', {}).get('address1', ''),
                'city': business_info.get('location', {}).get('city', ''),
                'state': business_info.get('location', {}).get('state', ''),
                'zip_code': business_info.get('location', {}).get('zip_code', ''),
                'rating': business_info.get('rating', 0),
                'review_count': business_info.get('review_count', 0),
                'price': business_info.get('price', ''),
                'categories': ', '.join([category['title'] for category in business_info.get('categories', [])]),
                'url': business_info.get('url', ''),
                'image_url': business_info.get('image_url', '')
            })
            conn.commit()
            conn.close()
            logging.info(f"Saved business: {business_info['name']}")
        except sqlite3.Error as e:
            logging.error(f"Failed to save data to the database: {e}")

    def save_progress(self, search_term, location, last_offset):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO yelp_progress (id, search_term, location, last_offset)
                VALUES ((SELECT id FROM yelp_progress WHERE search_term = ? AND location = ?), ?, ?, ?)
            ''', (search_term, location, search_term, location, last_offset))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logging.error(f"Failed to save progress: {e}")

    def get_last_offset(self, search_term, location):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT last_offset FROM yelp_progress WHERE search_term = ? AND location = ?
            ''', (search_term, location))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except sqlite3.Error as e:
            logging.error(f"Failed to retrieve last offset: {e}")
            return 0

    def get_total_entries(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM yelp')
            total_entries = cursor.fetchone()[0]
            conn.close()
            return total_entries
        except sqlite3.Error as e:
            logging.error(f"Failed to count entries in the database: {e}")
            return 0
