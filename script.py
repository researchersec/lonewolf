import requests
import json
from datetime import datetime
import os
import shutil

api_key = os.environ['API_KEY']

auth_url = 'https://auth.tradeskillmaster.com/oauth2/token'
alli_pricing_url = 'https://pricing-api.tradeskillmaster.com/ah/513'
horde_pricing_url = 'https://pricing-api.tradeskillmaster.com/ah/514'

#realm_url = 'https://realm-api.tradeskillmaster.com/regions'
#realm_data = 'https://realm-api.tradeskillmaster.com/regions/22/realms'

payload = {
    "client_id": "c260f00d-1071-409a-992f-dda2e5498536",
    "grant_type": "api_token",
    "scope": "app:realm-api app:pricing-api",
    "token": api_key
}

# Authenticate and get access token
response = requests.post(auth_url, json=payload)
if response.status_code == 201:
    auth_data = response.json()
    access_token = auth_data.get('access_token')
    print("Access token obtained successfully")

    # Headers for authentication
    headers = {'Authorization': f'Bearer {access_token}'}

    # Function to filter out unwanted keys
    def filter_data(pricing_data):
        if isinstance(pricing_data, list):
            return [
                {k: v for k, v in item.items() if k not in {"auctionHouseId", "petSpeciesId", "historical"}}
                for item in pricing_data
            ]
        elif isinstance(pricing_data, dict):
            return {k: v for k, v in pricing_data.items() if k not in {"auctionHouseId", "petSpeciesId", "historical"}}
        return pricing_data  # In case the format is unexpected

    # Fetch Horde pricing data
    horde_pricing_response = requests.get(horde_pricing_url, headers=headers)
    if horde_pricing_response.status_code == 200:
        raw_pricing_data = horde_pricing_response.json()
        pricing_data = filter_data(raw_pricing_data)  # Apply filtering

        with open("prices/latest.json", 'w') as file:
            json.dump({"pricing_data": pricing_data}, file, indent=4)
        with open("horde.json", 'w') as file:
            json.dump({"pricing_data": pricing_data}, file, indent=4)
        print("Horde pricing data saved successfully.")
    else:
        print("Failed to fetch horde pricing data")

    # Fetch Alliance pricing data
    alli_pricing_response = requests.get(alli_pricing_url, headers=headers)
    if alli_pricing_response.status_code == 200:
        raw_pricing_data = alli_pricing_response.json()
        pricing_data = filter_data(raw_pricing_data)  # Apply filtering

        with open("alli.json", 'w') as file:
            json.dump({"pricing_data": pricing_data}, file, indent=4)
        print("Alliance pricing data saved successfully.")
    else:
        print("Failed to fetch alliance pricing data")
else:
    print("Failed to obtain access token")
