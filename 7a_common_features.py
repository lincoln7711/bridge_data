import json
import os
from collections import defaultdict

def analyze_bridge_features(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 7a_data folder if it doesn't exist
    if not os.path.exists('7a_data'):
        os.makedirs('7a_data')

    features_carried = defaultdict(int)
    features_crossed = defaultdict(int)
    regional_features = defaultdict(lambda: {'carried': defaultdict(int), 'crossed': defaultdict(int)})
    county_features = defaultdict(lambda: {'carried': defaultdict(int), 'crossed': defaultdict(int)})

    for bridge in bridges:
        feature_carried = bridge['Feature Carried']
        feature_crossed = bridge['Feature Crossed']
        region = bridge['Region']
        county = bridge['County']

        features_carried[feature_carried] += 1
        features_crossed[feature_crossed] += 1
        regional_features[region]['carried'][feature_carried] += 1
        regional_features[region]['crossed'][feature_crossed] += 1
        county_features[county]['carried'][feature_carried] += 1
        county_features[county]['crossed'][feature_crossed] += 1

    # Write total results
    with open('7a_data/most_common_features_total.txt', 'w') as f:
        f.write("Most Common Features Carried:\n")
        for feature, count in sorted(features_carried.items(), key=lambda x: x[1], reverse=True)[:20]:
            f.write(f"{feature}: {count}\n")
        f.write("\nMost Common Features Crossed:\n")
        for feature, count in sorted(features_crossed.items(), key=lambda x: x[1], reverse=True)[:20]:
            f.write(f"{feature}: {count}\n")

    # Write regional results
    with open('7a_data/most_common_features_by_region.txt', 'w') as f:
        for region, features in regional_features.items():
            f.write(f"\nRegion: {region}\n")
            f.write("Most Common Features Carried:\n")
            for feature, count in sorted(features['carried'].items(), key=lambda x: x[1], reverse=True)[:10]:
                f.write(f"{feature}: {count}\n")
            f.write("Most Common Features Crossed:\n")
            for feature, count in sorted(features['crossed'].items(), key=lambda x: x[1], reverse=True)[:10]:
                f.write(f"{feature}: {count}\n")

    # Write county results
    with open('7a_data/most_common_features_by_county.txt', 'w') as f:
        for county, features in county_features.items():
            f.write(f"\nCounty: {county}\n")
            f.write("Most Common Features Carried:\n")
            for feature, count in sorted(features['carried'].items(), key=lambda x: x[1], reverse=True)[:5]:
                f.write(f"{feature}: {count}\n")
            f.write("Most Common Features Crossed:\n")
            for feature, count in sorted(features['crossed'].items(), key=lambda x: x[1], reverse=True)[:5]:
                f.write(f"{feature}: {count}\n")

    print("Feature analysis complete. Results saved in the '7a_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_bridge_features(json_file_path)
