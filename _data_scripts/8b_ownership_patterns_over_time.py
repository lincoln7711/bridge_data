import json
import os
from collections import defaultdict

def analyze_ownership_patterns(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 8a_data folder if it doesn't exist
    if not os.path.exists('8b_data'):
        os.makedirs('8b_data')

    # Group bridges by decade and owner
    decades = defaultdict(lambda: defaultdict(int))

    for bridge in bridges:
        year_built = bridge['Year Built or Replaced']
        owner = bridge['Owner']
        
        if year_built.isdigit():
            decade = (int(year_built) // 10) * 10
            decades[decade][owner] += 1

    # Write results to file
    with open('8b_data/ownership_patterns_over_time.txt', 'w') as f:
        f.write("Bridge Ownership Patterns Over Time:\n\n")
        for decade in sorted(decades.keys()):
            f.write(f"Decade: {decade}s\n")
            total_bridges = sum(decades[decade].values())
            for owner, count in sorted(decades[decade].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_bridges) * 100
                f.write(f"{owner}: {count} ({percentage:.2f}%)\n")
            f.write("\n")

    print("Ownership patterns over time analysis complete. Results saved in the '8b_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_ownership_patterns(json_file_path)
