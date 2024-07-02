import json
import os
from collections import defaultdict

def analyze_bridge_conditions_by_owner(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 5a_data folder if it doesn't exist
    if not os.path.exists('5a_data'):
        os.makedirs('5a_data')

    # Dictionary to store bridge conditions by owner
    owner_conditions = defaultdict(lambda: defaultdict(int))

    for bridge in bridges:
        owner = bridge['Owner']
        condition = 'Poor' if bridge['Poor Status'] == 'Y' else 'Not Poor'
        owner_conditions[owner][condition] += 1

    # Calculate percentages and prepare results
    results = []
    for owner, conditions in owner_conditions.items():
        total = conditions['Poor'] + conditions['Not Poor']
        poor_percentage = (conditions['Poor'] / total) * 100 if total > 0 else 0
        not_poor_percentage = (conditions['Not Poor'] / total) * 100 if total > 0 else 0
        
        results.append({
            'Owner': owner,
            'Total Bridges': total,
            'Poor Condition': conditions['Poor'],
            'Not Poor Condition': conditions['Not Poor'],
            'Poor Percentage': poor_percentage,
            'Not Poor Percentage': not_poor_percentage
        })

    # Sort results by total number of bridges (descending)
    results.sort(key=lambda x: x['Total Bridges'], reverse=True)

    # Write results to file
    with open('5a_data/bridge_conditions_by_owner.txt', 'w') as f:
        f.write("Bridge Conditions by Owner:\n")
        f.write("Owner, Total Bridges, Poor Condition, Not Poor Condition, Poor %, Not Poor %\n")
        for result in results:
            f.write(f"{result['Owner']}, {result['Total Bridges']}, {result['Poor Condition']}, "
                    f"{result['Not Poor Condition']}, {result['Poor Percentage']:.2f}%, "
                    f"{result['Not Poor Percentage']:.2f}%\n")

    print("Analysis complete. Results saved in the '5a_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_bridge_conditions_by_owner(json_file_path)
