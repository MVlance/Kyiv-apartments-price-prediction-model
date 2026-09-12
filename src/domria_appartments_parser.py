# parses features of one flat at a time

import requests
from datetime import datetime
import time
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

APARTMENT_IDS = []

current_dir = Path(__file__).parent
data_dir = current_dir / "data"
apartment_ids_file = data_dir / "apartment_ids.txt"

if not apartment_ids_file.exists():
    print("Apartment IDs file not found.")
    exit(0)

with open(apartment_ids_file, 'r', encoding='utf-8') as f:
    APARTMENT_IDS = [int(line.strip()) for line in f.readlines()]

print(f"{len(APARTMENT_IDS)} apartments left in queue.")

load_dotenv()
API_KEY = os.getenv("DOMRIA_API_KEY")

if not API_KEY:
    print("API_KEY not found.")
    exit(0)

params = {
    "api_key": API_KEY,
}

file_path = data_dir / "kyiv_apartments.csv"
file_exists = file_path.exists()

for apartment_id in list(APARTMENT_IDS):

    URL = f"https://developers.ria.com/dom/info/{apartment_id}"

    try:
        print(f"{datetime.now().strftime("%H:%M:%S on %B %d, %Y")}: Sending GET request to the server...")
        response = requests.get(URL, params=params)


        if response.status_code == 200:
            print(f"{datetime.now().strftime("%H:%M:%S on %B %d, %Y")}: Response status code: 200. Success!")

            data = response.json()

            apartment_info = {
                "apartment_id": apartment_id,
                "price_usd": data.get("price"),
                "total_area": data.get("total_square_meters"),
                "living_area": data.get("living_square_meters"),
                "kitchen_area": data.get("kitchen_square_meters"),
                "floor": data.get("floor"),
                "floors_count": data.get("floors_count"),
                "rooms_count": data.get("rooms_count"),
                "district": data.get("district_name"),
                "wall_type": data.get("wall_type"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
            }
            row_df = pd.DataFrame([apartment_info])
            row_df.to_csv(file_path, mode='a', index=False, header=not file_exists, encoding='utf-8')

            file_exists = True
            print(f"{datetime.now().strftime("%H:%M:%S on %B %d, %Y")}: Collected data for APARTMENT ID: {apartment_id}. Success!")

            APARTMENT_IDS.remove(apartment_id)

            with open(apartment_ids_file, 'w', encoding='utf-8') as f:
                for remaining_id in APARTMENT_IDS:
                    f.write(f"{remaining_id}\n")

            print(f"{datetime.now().strftime("%H:%M:%S on %B %d, %Y")}: Success! ID: {apartment_id} has been collected and deleted from memory!")

        elif response.status_code == 429: #too many attempts
            print(f"{datetime.now().strftime("%H:%M:%S on %B %d, %Y")}: Response status code: 429. Retrying in 5 minutes...")
            time.sleep(300)
        else:
            print("Error. Status code: {response.status_code}")
            print("Status message: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"{datetime.now().strftime("%H:%M:%S on %B %d, %Y")}: Internet connection error: {e}")

    print(f"{datetime.now().strftime("%H:%M:%S on %B %d, %Y")}: Waiting 125 seconds for the next request...")
    time.sleep(125)


print(f"{datetime.now().strftime("%H:%M:%S on %B %d, %Y")}: Success! Parsing is finished!")