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

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f'{timestamp}.json'

# Request body for access token
payload = {
    "client_id": "c260f00d-1071-409a-992f-dda2e5498536",
    "grant_type": "api_token",
    "scope": "app:realm-api app:pricing-api",
    "token": api_key
}

# Get access token
response = requests.post(auth_url, json=payload)
if response.status_code == 201:
    auth_data = response.json()
    access_token = auth_data.get('access_token')
    print("Access token obtained successfully")

    # Make GET request for pricing data
    headers = {'Authorization': f'Bearer {access_token}'}
    pricing_response = requests.get(pricing_url, headers=headers)
    if pricing_response.status_code == 200:
        pricing_data = pricing_response.json()
        print("Pricing data obtained successfully")

        # Connect to SQLite database
        conn = sqlite3.connect('pricing_data.db')
        cursor = conn.cursor()

        # Create a table if not exists
        cursor.execute('''CREATE TABLE IF NOT EXISTS pricing (
                            itemId INTEGER PRIMARY KEY,
                            timestamp TEXT,
                            minBuyout INTEGER,
                            quantity INTEGER,
                            marketValue INTEGER,
                            historical INTEGER,
                            numAuctions INTEGER
                        )''')

        # Insert pricing data into the SQLite database with timestamp
        for item in pricing_data['pricing_data']:
            # Exclude unwanted fields (auctionHouseId and petSpeciesId)
            item.pop('auctionHouseId', None)
            item.pop('petSpeciesId', None)

            # Insert data into the SQLite table with current timestamp
            cursor.execute('''INSERT INTO pricing (itemId, timestamp, minBuyout, quantity, marketValue, historical, numAuctions)
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (item['itemId'], timestamp, item['minBuyout'], item['quantity'], item['marketValue'],
                            item['historical'], item['numAuctions']))

        # Commit changes to the database
        conn.commit()

        # Close the connection
        conn.close()
    else:
        print("Failed to fetch pricing data")
else:
    print("Failed to obtain access token")
