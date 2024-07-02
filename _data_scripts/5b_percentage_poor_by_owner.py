import json
import os
from collections import defaultdict

def analyze_poor_bridges_by_owner(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 5b_data folder if it doesn't exist
    if not os.path.exists('5b_data'):
        os.makedirs('5b_data')

    # Dictionary to store bridge counts by owner
    owner_counts = defaultdict(lambda: {'total': 0, 'poor': 0})

    for bridge in bridges:
        owner = bridge['Owner']
        owner_counts[owner]['total'] += 1
        if bridge['Poor Status'] == 'Y':
            owner_counts[owner]['poor'] += 1

    # Calculate percentages and prepare results
    results = []
    for owner, counts in owner_counts.items():
        poor_percentage = (counts['poor'] / counts['total']) * 100 if counts['total'] > 0 else 0
        results.append({
            'Owner': owner,
            'Total Bridges': counts['total'],
            'Poor Condition Bridges': counts['poor'],
            'Poor Percentage': poor_percentage
        })

    # Sort results by poor percentage (descending)
    results.sort(key=lambda x: x['Poor Percentage'], reverse=True)

    # Write results to file
    with open('5b_data/poor_bridges_percentage_by_owner.txt', 'w') as f:
        f.write("Percentage of Poor Condition Bridges by Owner:\n")
        f.write("Owner, Total Bridges, Poor Condition Bridges, Poor %\n")
        for result in results:
            f.write(f"{result['Owner']}, {result['Total Bridges']}, {result['Poor Condition Bridges']}, "
                    f"{result['Poor Percentage']:.2f}%\n")

    print("Analysis complete. Results saved in the '5b_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_poor_bridges_by_owner(json_file_path)

