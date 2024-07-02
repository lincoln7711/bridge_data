import json
import os
from datetime import datetime
from collections import defaultdict

def analyze_average_bridge_age(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 6b_data folder if it doesn't exist
    if not os.path.exists('6b_data'):
        os.makedirs('6b_data')

    current_year = datetime.now().year
    owner_ages = defaultdict(list)
    region_ages = defaultdict(list)

    for bridge in bridges:
        year_built = bridge['Year Built or Replaced']
        if year_built.isdigit():
            age = current_year - int(year_built)
            owner = bridge['Owner']
            region = bridge['Region']
            
            owner_ages[owner].append(age)
            region_ages[region].append(age)

    # Calculate average age by owner
    with open('6b_data/average_age_by_owner.txt', 'w') as f:
        f.write("Average Bridge Age by Owner:\n")
        f.write("Owner, Average Age (years), Number of Bridges\n")
        for owner, ages in sorted(owner_ages.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
            avg_age = sum(ages) / len(ages)
            f.write(f"{owner}, {avg_age:.2f}, {len(ages)}\n")

    # Calculate average age by region
    with open('6b_data/average_age_by_region.txt', 'w') as f:
        f.write("Average Bridge Age by Region:\n")
        f.write("Region, Average Age (years), Number of Bridges\n")
        for region, ages in sorted(region_ages.items(), key=lambda x: sum(x[1])/len(x[1]), reverse=True):
            avg_age = sum(ages) / len(ages)
            f.write(f"{region}, {avg_age:.2f}, {len(ages)}\n")

    print("Average age analysis complete. Results saved in the '6b_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_average_bridge_age(json_file_path)
