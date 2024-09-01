import sqlite3
import logging

class YPDatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def setup_database(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS yellow_pages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    phone TEXT,
                    address TEXT,
                    city TEXT,
                    state TEXT,
                    zip TEXT,
                    type TEXT,
                    notes TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS yp_progress (
                    id INTEGER PRIMARY KEY,
                    location TEXT,
                    last_page INTEGER
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
                SELECT 1 FROM yellow_pages WHERE name = :name AND phone = :phone AND address = :address AND city = :city AND state = :state AND zip = :zip
            ''', business_info)
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
                INSERT INTO yellow_pages (name, phone, address, city, state, zip, type, notes)
                VALUES (:name, :phone, :address, :city, :state, :zip, :type, :notes)
            ''', business_info)
            conn.commit()
            conn.close()
            logging.info(f"Saved business: {business_info['name']}")
        except sqlite3.Error as e:
            logging.error(f"Failed to save data to the database: {e}")

    def save_progress(self, location, last_page):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO yp_progress (id, location, last_page)
                VALUES ((SELECT id FROM yp_progress WHERE location = ?), ?, ?)
            ''', (location, location, last_page))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            logging.error(f"Failed to save progress: {e}")

    def get_last_page(self, location):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                SELECT last_page FROM yp_progress WHERE location = ?
            ''', (location,))
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 1
        except sqlite3.Error as e:
            logging.error(f"Failed to retrieve last page: {e}")
            return 1

    def get_total_entries(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM yellow_pages')
            total_entries = cursor.fetchone()[0]
            conn.close()
            return total_entries
        except sqlite3.Error as e:
            logging.error(f"Failed to count entries in the database: {e}")
            return 0
