import json
import os
from collections import defaultdict

def identify_critical_bridges(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 9_data folder if it doesn't exist
    if not os.path.exists('9_data'):
        os.makedirs('9_data')

    # Define criteria for critical bridges
    major_routes = ['I-', 'US ', 'NY ']  # Interstate, US, and NY state highways
    significant_features = ['HUDSON RIVER', 'MOHAWK RIVER', 'LAKE', 'RAILROAD', 'CSX', 'AMTRAK']

    critical_bridges = []
    for bridge in bridges:
        is_critical = False
        reason = []

        # Check if the bridge is on a major route
        if any(route in bridge['Feature Carried'] for route in major_routes):
            is_critical = True
            reason.append("Major Route")

        # Check if the bridge crosses a significant feature
        if any(feature.upper() in bridge['Feature Crossed'].upper() for feature in significant_features):
            is_critical = True
            reason.append("Significant Feature")

        if is_critical:
            critical_bridges.append({
                'BIN': bridge['BIN'],
                'Feature Carried': bridge['Feature Carried'],
                'Feature Crossed': bridge['Feature Crossed'],
                'Year Built': bridge['Year Built or Replaced'],
                'Last Inspection': bridge['Date of Last Inspection'],
                'Poor Condition': 'Yes' if bridge['Poor Status'] == 'Y' else 'No',
                'Reason': ', '.join(reason)
            })

    # Sort critical bridges by condition (poor first) and then by year built (oldest first)
    critical_bridges.sort(key=lambda x: (x['Poor Condition'] == 'No', x['Year Built']), reverse=True)

    # Write results to file
    with open('9_data/critical_bridges_analysis.txt', 'w') as f:
        f.write("Critical Infrastructure Bridges Analysis:\n\n")
        f.write("Total Critical Bridges Identified: {}\n".format(len(critical_bridges)))
        f.write("Poor Condition Critical Bridges: {}\n\n".format(sum(1 for bridge in critical_bridges if bridge['Poor Condition'] == 'Yes')))
        
        f.write("Detailed List of Critical Bridges:\n")
        f.write("BIN, Feature Carried, Feature Crossed, Year Built, Last Inspection, Poor Condition, Reason\n")
        for bridge in critical_bridges:
            f.write("{},{},{},{},{},{},{}\n".format(
                bridge['BIN'],
                bridge['Feature Carried'],
                bridge['Feature Crossed'],
                bridge['Year Built'],
                bridge['Last Inspection'],
                bridge['Poor Condition'],
                bridge['Reason']
            ))

    print("Critical infrastructure analysis complete. Results saved in the '9_data' folder.")

    # Additional analysis: Age distribution of critical bridges
    age_distribution = defaultdict(int)
    current_year = 2024  # Update this to the current year
    for bridge in critical_bridges:
        age = current_year - int(bridge['Year Built'])
        age_group = (age // 10) * 10
        age_distribution[age_group] += 1

    with open('9_data/critical_bridges_age_distribution.txt', 'w') as f:
        f.write("Age Distribution of Critical Bridges:\n\n")
        for age_group in sorted(age_distribution.keys()):
            f.write("{}-{} years: {}\n".format(age_group, age_group + 9, age_distribution[age_group]))

# Usage
json_file_path = 'bridge_conditions.json'
identify_critical_bridges(json_file_path)
