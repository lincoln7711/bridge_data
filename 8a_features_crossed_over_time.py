import json
import os
from collections import defaultdict

def analyze_features_crossed_over_time(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 8a_data folder if it doesn't exist
    if not os.path.exists('8a_data'):
        os.makedirs('8a_data')

    # Group bridges by decade and feature crossed
    decades = defaultdict(lambda: defaultdict(int))

    for bridge in bridges:
        year_built = bridge['Year Built or Replaced']
        feature_crossed = bridge['Feature Crossed']
        
        if year_built.isdigit():
            decade = (int(year_built) // 10) * 10
            decades[decade][feature_crossed] += 1

    # Write results to file
    with open('8a_data/features_crossed_over_time.txt', 'w') as f:
        f.write("Features Crossed by Bridges Over Time:\n\n")
        for decade in sorted(decades.keys()):
            f.write(f"Decade: {decade}s\n")
            total_bridges = sum(decades[decade].values())
            for feature, count in sorted(decades[decade].items(), key=lambda x: x[1], reverse=True)[:10]:
                percentage = (count / total_bridges) * 100
                f.write(f"{feature}: {count} ({percentage:.2f}%)\n")
            f.write("\n")

    print("Features crossed over time analysis complete. Results saved in the '8a_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_features_crossed_over_time(json_file_path)
