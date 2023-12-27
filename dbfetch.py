import requests
import json
from datetime import datetime
import os
import sqlite3

api_key = os.environ['API_KEY']
# Endpoint URLs
auth_url = 'https://auth.tradeskillmaster.com/oauth2/token'
pricing_url = 'https://pricing-api.tradeskillmaster.com/ah/512'
realm_url = 'https://realm-api.tradeskillmaster.com/regions'

# Connect to SQLite database
conn = sqlite3.connect('pricing_data.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pricing_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER,
        item_name TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS pricing_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pricing_id INTEGER,
        item_id INTEGER,
        price INTEGER,
        FOREIGN KEY(pricing_id) REFERENCES pricing_data(id),
        FOREIGN KEY(item_id) REFERENCES items(id)
    )
''')

conn.commit()

# Request body for access token
payload = {
    "client_id": "c260f00d-1071-409a-992f-dda2e5498536",
    "grant_type": "api_token",
    "scope": "app:realm-api app:pricing-api",
    "token": api_key
}

response = requests.post(auth_url, json=payload)
if response.status_code == 201:
    auth_data = response.json()
    access_token = auth_data.get('access_token')
    print("Access token obtained successfully")

    headers = {'Authorization': f'Bearer {access_token}'}
    pricing_response = requests.get(pricing_url, headers=headers)
    if pricing_response.status_code == 200:
        pricing_data = pricing_response.json()
        print("Pricing data obtained successfully")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert timestamp into pricing_data table
        cursor.execute('''
            INSERT INTO pricing_data (timestamp)
            VALUES (?)
        ''', (timestamp,))
        pricing_id = cursor.lastrowid  # Get the last inserted row ID

        # Process pricing details and insert into pricing_details table
        for item in pricing_data:
            item_id = item.get('item_id')
            item_name = item.get('item_name')
            price = item.get('price')

            # Check if the item exists in the items table, if not, add it
            cursor.execute('''
                SELECT id FROM items WHERE item_id = ?
            ''', (item_id,))
            item_row = cursor.fetchone()

            if not item_row:
                cursor.execute('''
                    INSERT INTO items (item_id, item_name)
                    VALUES (?, ?)
                ''', (item_id, item_name))
                conn.commit()  # Commit the item addition

                # Retrieve the newly inserted item's ID
                cursor.execute('''
                    SELECT id FROM items WHERE item_id = ?
                ''', (item_id,))
                item_row = cursor.fetchone()

            if item_row:
                item_id_db = item_row[0]

                # Insert pricing details into pricing_details table
                cursor.execute('''
                    INSERT INTO pricing_details (pricing_id, item_id, price)
                    VALUES (?, ?, ?)
                ''', (pricing_id, item_id_db, price))
                conn.commit()  # Commit the pricing details
            else:
                print(f"Failed to add or retrieve item: {item_id} - {item_name}")

    else:
        print("Failed to fetch pricing data")
else:
    print("Failed to obtain access token")

conn.close()  # Close the database connection when finished
