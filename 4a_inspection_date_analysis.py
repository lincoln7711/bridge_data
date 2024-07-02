import json
import os
from collections import defaultdict
from datetime import datetime

def analyze_inspection_dates(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 4a_data folder if it doesn't exist
    if not os.path.exists('4a_data'):
        os.makedirs('4a_data')

    # Dictionary to store inspection counts by year and month
    inspection_counts = defaultdict(int)

    for bridge in bridges:
        inspection_date = bridge['Date of Last Inspection']
        try:
            # Parse the date and extract year and month
            date = datetime.strptime(inspection_date, '%m/%d/%Y')
            year_month = date.strftime('%Y-%m')
            inspection_counts[year_month] += 1
        except ValueError:
            # Skip invalid date formats
            continue

    # Sort the results chronologically
    sorted_counts = sorted(inspection_counts.items())

    # Write results to file
    with open('4a_data/inspection_date_distribution.txt', 'w') as f:
        f.write("Distribution of Last Inspection Dates (Year-Month):\n")
        f.write("Year-Month, Number of Inspections\n")
        for year_month, count in sorted_counts:
            f.write(f"{year_month}, {count}\n")

    print("Analysis complete. Results saved in the '4a_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_inspection_dates(json_file_path)
