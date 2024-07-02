import json
import os
from collections import defaultdict

def calculate_poor_bridge_percentage(bridges):
    total_bridges = len(bridges)
    poor_bridges = sum(1 for bridge in bridges if bridge['Poor Status'] == 'Y')
    poor_percentage = (poor_bridges / total_bridges) * 100 if total_bridges > 0 else 0
    return total_bridges, poor_bridges, poor_percentage

def analyze_bridges(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 1_data folder if it doesn't exist
    if not os.path.exists('1_data'):
        os.makedirs('1_data')

    # Overall statistics
    total, poor, percentage = calculate_poor_bridge_percentage(bridges)
    with open('1_data/total_statistics.txt', 'w') as f:
        f.write(f"Overall Statistics:\n")
        f.write(f"Total bridges: {total}\n")
        f.write(f"Poor condition bridges: {poor}\n")
        f.write(f"Percentage in poor condition: {percentage:.2f}%\n")

    # By Region
    regions = defaultdict(list)
    for bridge in bridges:
        regions[bridge['Region']].append(bridge)

    with open('1_data/region_statistics.txt', 'w') as f:
        f.write("Statistics by Region:\n")
        for region, region_bridges in regions.items():
            total, poor, percentage = calculate_poor_bridge_percentage(region_bridges)
            f.write(f"Region {region}: Total: {total}, Poor: {poor}, Percentage: {percentage:.2f}%\n")

    # By County
    counties = defaultdict(list)
    for bridge in bridges:
        counties[bridge['County']].append(bridge)

    with open('1_data/county_statistics.txt', 'w') as f:
        f.write("Statistics by County:\n")
        for county, county_bridges in counties.items():
            total, poor, percentage = calculate_poor_bridge_percentage(county_bridges)
            f.write(f"{county} County: Total: {total}, Poor: {poor}, Percentage: {percentage:.2f}%\n")

    # By Municipality
    municipalities = defaultdict(list)
    for bridge in bridges:
        municipalities[bridge['Municipality']].append(bridge)

    with open('1_data/municipality_statistics.txt', 'w') as f:
        f.write("Statistics by Municipality:\n")
        for municipality, municipality_bridges in municipalities.items():
            total, poor, percentage = calculate_poor_bridge_percentage(municipality_bridges)
            f.write(f"{municipality}: Total: {total}, Poor: {poor}, Percentage: {percentage:.2f}%\n")

    print("Analysis complete. Results saved in the '1_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_bridges(json_file_path)
