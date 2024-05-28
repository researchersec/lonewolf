import os
import json
import sqlite3
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 1: Create the SQLite database and table
conn = sqlite3.connect('prices.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS prices (
    itemId INTEGER,
    minBuyout INTEGER,
    quantity INTEGER,
    marketValue INTEGER,
    historical INTEGER,
    numAuctions INTEGER,
    filename_timestamp TEXT
)
''')
conn.commit()

# Step 2: Function to insert data into the database
def insert_data(data):
    with conn:
        c.execute('''
        INSERT INTO prices (itemId, minBuyout, quantity, marketValue, historical, numAuctions, filename_timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', data)
    logging.info(f"Inserted data: {data}")

# Function to check if a filename is a valid timestamp and return it
def get_timestamp_from_filename(filename):
    try:
        timestamp_str = filename.split('.')[0]
        datetime.strptime(timestamp_str, '%Y-%m-%d_%H-%M-%S')
        return timestamp_str
    except ValueError:
        return None

# Step 3: Read JSON files and extract data
directory = '/prices/'

for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        timestamp = get_timestamp_from_filename(filename)
        if timestamp:
            logging.info(f"Processing file: {filepath}")
            with open(filepath, 'r') as file:
                content = json.load(file)
                for item in content['pricing_data']:
                    data = (
                        item['itemId'],
                        item['minBuyout'],
                        item['quantity'],
                        item['marketValue'],
                        item['historical'],
                        item['numAuctions'],
                        timestamp
                    )
                    insert_data(data)
        else:
            logging.warning(f"Skipping file with invalid timestamp: {filepath}")

# Step 4: Commit and close the connection
conn.commit()
conn.close()

logging.info("Data insertion completed.")
