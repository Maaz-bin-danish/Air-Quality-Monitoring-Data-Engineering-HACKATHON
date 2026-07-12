import requests
import os
from dotenv import load_dotenv
import pandas as pd

# Load API Key
load_dotenv()

API_KEY = os.getenv("OPENAQ_API_KEY")

headers = {
    "X-API-Key": API_KEY
}

url = "https://api.openaq.org/v3/locations"

# Filter ONLY Pakistan
params = {
    "iso": "PK",
    "limit": 100,
    "page": 1
}

response = requests.get(url, headers=headers, params=params)

print("Status Code:", response.status_code)

if response.status_code == 200:

    data = response.json()

    results = data["results"]

    print("Total Locations Found:", len(results))

    records = []

    for location in results:

        records.append({
            "Location ID": location["id"],
            "Location Name": location["name"],
            "City": location["locality"],
            "Country": location["country"]["code"],
            "Latitude": location["coordinates"]["latitude"],
            "Longitude": location["coordinates"]["longitude"]
        })

    df = pd.DataFrame(records)

    print(df.to_string(index=False))

    df.to_csv("openaq_locations.csv", index=False)

    print("\nCSV Saved Successfully!")

else:
    print(response.text)