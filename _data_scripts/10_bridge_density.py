import json
import os
from collections import defaultdict

def calculate_bridge_density(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 10_data folder if it doesn't exist
    if not os.path.exists('10_data'):
        os.makedirs('10_data')

    # Count bridges by county and municipality
    county_counts = defaultdict(int)
    municipality_counts = defaultdict(int)

    for bridge in bridges:
        county = bridge['County']
        municipality = bridge['Municipality']
        county_counts[county] += 1
        municipality_counts[(county, municipality)] += 1

    # Write county results
    with open('10_data/bridge_density_by_county.txt', 'w') as f:
        f.write("Bridge Density by County:\n")
        f.write("County, Number of Bridges\n")
        for county, count in sorted(county_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{county}, {count}\n")

    # Write municipality results
    with open('10_data/bridge_density_by_municipality.txt', 'w') as f:
        f.write("Bridge Density by Municipality:\n")
        f.write("County, Municipality, Number of Bridges\n")
        for (county, municipality), count in sorted(municipality_counts.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{county}, {municipality}, {count}\n")

    print("Bridge density analysis complete. Results saved in the '10_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
calculate_bridge_density(json_file_path)
