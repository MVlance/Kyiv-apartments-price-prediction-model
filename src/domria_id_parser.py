# pretty self-explanatory

import os
import requests
from datetime import datetime
from dotenv import load_dotenv

url = "https://developers.ria.com/dom/search"
load_dotenv()
API_KEY = os.getenv("DOMRIA_API_KEY")

if not API_KEY:
    print("API_KEY not found.")
    exit(0)

params = {
    "api_key": API_KEY,
    "category": 1,                 #flats
    "reality_type": 2,             #flat
    "operation_type": 1,           #selling
    "state_id": 10,                #kyiv state
    "city_id": 10,                 #Kyiv city
    "characteristics[242]": 239,   #usd
    "page": 9
}

print(f"{datetime.now().strftime("%H:%M:%S on %B %d, %Y")}: Sending GET request to the server...")

response = requests.get(url, params=params)

if response.status_code == 200:
    print(f"{datetime.now().strftime("%H:%M:%S on %B %d, %Y")}: Response status code: 200. Success!")

    data = response.json()
    total_count = data.get("count")
    apartment_ids = data.get("items")

    print(f"Total number of apartments: {total_count}")
    print(f"Apartment IDs: {apartment_ids}")
else:
    print(f"Error. Status code: {response.status_code}")
    print(f"Error. Response text: {response.text}")