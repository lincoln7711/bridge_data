import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    # Read the CSV file
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)

    # Write the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print(f"Conversion complete. JSON file saved as {json_file_path}")

# Usage
csv_file_path = 'Bridge_Conditions__NYS_Department_of_Transportation_20240702.csv'
json_file_path = 'bridge_conditions.json'

csv_to_json(csv_file_path, json_file_path)
