import json
import os
from datetime import datetime
from collections import defaultdict

def analyze_bridge_age_distribution(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 6a_data folder if it doesn't exist
    if not os.path.exists('6a_data'):
        os.makedirs('6a_data')

    current_year = datetime.now().year
    age_distribution = defaultdict(int)
    age_groups = defaultdict(int)

    for bridge in bridges:
        year_built = bridge['Year Built or Replaced']
        if year_built.isdigit():
            age = current_year - int(year_built)
            age_distribution[age] += 1

            # Group ages
            if age < 10:
                age_groups['0-9 years'] += 1
            elif age < 25:
                age_groups['10-24 years'] += 1
            elif age < 50:
                age_groups['25-49 years'] += 1
            elif age < 75:
                age_groups['50-74 years'] += 1
            elif age < 100:
                age_groups['75-99 years'] += 1
            else:
                age_groups['100+ years'] += 1

    # Write detailed age distribution
    with open('6a_data/bridge_age_distribution.txt', 'w') as f:
        f.write("Bridge Age Distribution:\n")
        f.write("Age (years), Number of Bridges\n")
        for age in sorted(age_distribution.keys()):
            f.write(f"{age}, {age_distribution[age]}\n")

    # Write age group distribution
    with open('6a_data/bridge_age_groups.txt', 'w') as f:
        f.write("Bridge Age Group Distribution:\n")
        f.write("Age Group, Number of Bridges\n")
        for group in ['0-9 years', '10-24 years', '25-49 years', '50-74 years', '75-99 years', '100+ years']:
            f.write(f"{group}, {age_groups[group]}\n")

    print("Age distribution analysis complete. Results saved in the '6a_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_bridge_age_distribution(json_file_path)
