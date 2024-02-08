import requests
import json
from datetime import datetime
import os
import shutil

api_key = os.environ['API_KEY']
# Endpoint URLs
auth_url = 'https://auth.tradeskillmaster.com/oauth2/token'
pricing_url = 'https://pricing-api.tradeskillmaster.com/ah/512'
realm_url = 'https://realm-api.tradeskillmaster.com/regions'

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f'{timestamp}.json'
directory = 'prices'

# Specify the full path for the file
file_path = os.path.join(directory, filename)
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

        # Save pricing data to items.json
        with open(file_path, 'w') as file:
            json.dump({"pricing_data": pricing_data}, file, indent=4)

        # Specify the path for the latest file
        latest_file_path = os.path.join(directory, 'latest.json')

        # Copy the content of timestamp.json to latest.json
        try:
            shutil.move(file_path, latest_file_path)
            print("latest.json has been updated with the same data as timestamp.json.")
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
    else:
        print("Failed to fetch pricing data")
else:
    print("Failed to obtain access token")
