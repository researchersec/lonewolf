import requests
import json
from datetime import datetime
import os

api_key = os.environ['API_KEY']
# Endpoint URLs
auth_url = 'https://auth.tradeskillmaster.com/oauth2/token'
pricing_url = 'https://pricing-api.tradeskillmaster.com/ah/512'
realm_url = 'https://realm-api.tradeskillmaster.com/regions'

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

        timestamp = datetime.now().strftime("%Y-%m-%d")
        filename = f'pricing_data_{timestamp}.json'

        try:
            with open(filename, 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []

        existing_data.append({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pricing_data": pricing_data})

        with open(filename, 'w') as file:
            json.dump(existing_data, file, indent=4)
    else:
        print("Failed to fetch pricing data")
else:
    print("Failed to obtain access token")
