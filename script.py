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


response = requests.post(auth_url, json=payload)
if response.status_code == 201:
    auth_data = response.json()
    access_token = auth_data.get('access_token')
    print("Access token obtained successfully")

    # Make GET request for pricing data
    headers = {'Authorization': f'Bearer {access_token}'}
    horde_pricing_response = requests.get(horde_pricing_url, headers=headers)
    if horde_pricing_response.status_code == 200:
        pricing_data = horde_pricing_response.json()
        print("Pricing data obtained successfully")

        # Save pricing data to items.json
        with open("latest.json", 'w') as file:
            json.dump({"pricing_data": pricing_data}, file, indent=4)
        print("latest.json has been updated with the same data as timestamp.json.")
        with open("horde.json", 'w') as file:
            json.dump({"pricing_data": pricing_data}, file, indent=4)
        print("latest.json has been updated with the same data as timestamp.json.")
    else:
        print("Failed to fetch horde pricing data")
    alli_pricing_response = requests.get(alli_pricing_url, headers=headers)
    if alli_pricing_response.status_code == 200:
        pricing_data = alli_pricing_response.json()
        print("Pricing data obtained successfully")

        # Save pricing data to items.json
        with open("alli.json", 'w') as file:
            json.dump({"pricing_data": pricing_data}, file, indent=4)
        print("latest.json has been updated with the same data as timestamp.json.")
    else:
        print("Failed to fetch horde pricing data")
else:
    print("Failed to obtain horde access token")
