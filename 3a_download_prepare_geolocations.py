import requests
import json
import os

def download_geojson_data():
    # Create 3a_data folder if it doesn't exist
    if not os.path.exists('3a_data'):
        os.makedirs('3a_data')

    # Download the GeoJSON data
    url = "https://gisportalny.dot.ny.gov/hostingny/rest/services/Asset/NYSDOT_Structures/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
    response = requests.get(url)
    geojson_data = response.json()

    # Save the GeoJSON data to a file
    with open('3a_data/nysdot_bridges.geojson', 'w') as f:
        json.dump(geojson_data, f)

    print("GeoJSON data downloaded and saved in the '3a_data' folder.")

if __name__ == "__main__":
    download_geojson_data()
