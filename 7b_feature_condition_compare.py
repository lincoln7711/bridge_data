import json
import os
from collections import defaultdict

def analyze_feature_condition_correlation(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 7b_data folder if it doesn't exist
    if not os.path.exists('7b_data'):
        os.makedirs('7b_data')

    feature_carried_condition = defaultdict(lambda: {'total': 0, 'poor': 0})
    feature_crossed_condition = defaultdict(lambda: {'total': 0, 'poor': 0})
    regional_correlation = defaultdict(lambda: {
        'carried': defaultdict(lambda: {'total': 0, 'poor': 0}),
        'crossed': defaultdict(lambda: {'total': 0, 'poor': 0})
    })
    county_correlation = defaultdict(lambda: {
        'carried': defaultdict(lambda: {'total': 0, 'poor': 0}),
        'crossed': defaultdict(lambda: {'total': 0, 'poor': 0})
    })

    for bridge in bridges:
        feature_carried = bridge['Feature Carried']
        feature_crossed = bridge['Feature Crossed']
        is_poor = bridge['Poor Status'] == 'Y'
        region = bridge['Region']
        county = bridge['County']

        feature_carried_condition[feature_carried]['total'] += 1
        feature_crossed_condition[feature_crossed]['total'] += 1
        if is_poor:
            feature_carried_condition[feature_carried]['poor'] += 1
            feature_crossed_condition[feature_crossed]['poor'] += 1

        regional_correlation[region]['carried'][feature_carried]['total'] += 1
        regional_correlation[region]['crossed'][feature_crossed]['total'] += 1
        county_correlation[county]['carried'][feature_carried]['total'] += 1
        county_correlation[county]['crossed'][feature_crossed]['total'] += 1
        if is_poor:
            regional_correlation[region]['carried'][feature_carried]['poor'] += 1
            regional_correlation[region]['crossed'][feature_crossed]['poor'] += 1
            county_correlation[county]['carried'][feature_carried]['poor'] += 1
            county_correlation[county]['crossed'][feature_crossed]['poor'] += 1

    # Write total results
    with open('7b_data/feature_condition_correlation_total.txt', 'w') as f:
        f.write("Feature Carried Condition Correlation:\n")
        for feature, condition in sorted(feature_carried_condition.items(), key=lambda x: x[1]['total'], reverse=True):
            poor_percentage = (condition['poor'] / condition['total']) * 100 if condition['total'] > 0 else 0
            f.write(f"{feature}: Total: {condition['total']}, Poor: {condition['poor']}, Poor %: {poor_percentage:.2f}%\n")
        
        f.write("\nFeature Crossed Condition Correlation:\n")
        for feature, condition in sorted(feature_crossed_condition.items(), key=lambda x: x[1]['total'], reverse=True):
            poor_percentage = (condition['poor'] / condition['total']) * 100 if condition['total'] > 0 else 0
            f.write(f"{feature}: Total: {condition['total']}, Poor: {condition['poor']}, Poor %: {poor_percentage:.2f}%\n")

    # Write regional results
    with open('7b_data/feature_condition_correlation_by_region.txt', 'w') as f:
        for region, features in regional_correlation.items():
            f.write(f"\nRegion: {region}\n")
            f.write("Feature Carried Condition Correlation:\n")
            for feature, condition in sorted(features['carried'].items(), key=lambda x: x[1]['total'], reverse=True)[:10]:
                poor_percentage = (condition['poor'] / condition['total']) * 100 if condition['total'] > 0 else 0
                f.write(f"{feature}: Total: {condition['total']}, Poor: {condition['poor']}, Poor %: {poor_percentage:.2f}%\n")
            f.write("Feature Crossed Condition Correlation:\n")
            for feature, condition in sorted(features['crossed'].items(), key=lambda x: x[1]['total'], reverse=True)[:10]:
                poor_percentage = (condition['poor'] / condition['total']) * 100 if condition['total'] > 0 else 0
                f.write(f"{feature}: Total: {condition['total']}, Poor: {condition['poor']}, Poor %: {poor_percentage:.2f}%\n")

    # Write county results
    with open('7b_data/feature_condition_correlation_by_county.txt', 'w') as f:
        for county, features in county_correlation.items():
            f.write(f"\nCounty: {county}\n")
            f.write("Feature Carried Condition Correlation:\n")
            for feature, condition in sorted(features['carried'].items(), key=lambda x: x[1]['total'], reverse=True)[:5]:
                poor_percentage = (condition['poor'] / condition['total']) * 100 if condition['total'] > 0 else 0
                f.write(f"{feature}: Total: {condition['total']}, Poor: {condition['poor']}, Poor %: {poor_percentage:.2f}%\n")
            f.write("Feature Crossed Condition Correlation:\n")
            for feature, condition in sorted(features['crossed'].items(), key=lambda x: x[1]['total'], reverse=True)[:5]:
                poor_percentage = (condition['poor'] / condition['total']) * 100 if condition['total'] > 0 else 0
                f.write(f"{feature}: Total: {condition['total']}, Poor: {condition['poor']}, Poor %: {poor_percentage:.2f}%\n")

    print("Feature-condition correlation analysis complete. Results saved in the '7b_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_feature_condition_correlation(json_file_path)
