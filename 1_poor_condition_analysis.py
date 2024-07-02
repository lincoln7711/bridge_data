import json
from collections import defaultdict

def calculate_poor_bridge_percentage(bridges, category=None, category_value=None):
    if category and category_value:
        filtered_bridges = [bridge for bridge in bridges if bridge[category] == category_value]
    else:
        filtered_bridges = bridges

    total_bridges = len(filtered_bridges)
    poor_bridges = sum(1 for bridge in filtered_bridges if bridge['Poor Status'] == 'Y')
    
    if total_bridges == 0:
        return 0, 0, 0
    
    poor_percentage = (poor_bridges / total_bridges) * 100
    return total_bridges, poor_bridges, poor_percentage

def analyze_bridges(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Overall statistics
    total, poor, percentage = calculate_poor_bridge_percentage(bridges)
    print(f"Overall Statistics:")
    print(f"Total bridges: {total}")
    print(f"Poor condition bridges: {poor}")
    print(f"Percentage in poor condition: {percentage:.2f}%\n")

    # By Region
    regions = defaultdict(list)
    for bridge in bridges:
        regions[bridge['Region']].append(bridge)

    print("Statistics by Region:")
    for region, region_bridges in regions.items():
        total, poor, percentage = calculate_poor_bridge_percentage(region_bridges)
        print(f"Region {region}: Total: {total}, Poor: {poor}, Percentage: {percentage:.2f}%")
    print()

    # By County
    counties = defaultdict(list)
    for bridge in bridges:
        counties[bridge['County']].append(bridge)

    print("Statistics by County:")
    for county, county_bridges in counties.items():
        total, poor, percentage = calculate_poor_bridge_percentage(county_bridges)
        print(f"{county} County: Total: {total}, Poor: {poor}, Percentage: {percentage:.2f}%")
    print()

    # By Municipality
    municipalities = defaultdict(list)
    for bridge in bridges:
        municipalities[bridge['Municipality']].append(bridge)

    print("Statistics by Municipality:")
    for municipality, municipality_bridges in municipalities.items():
        total, poor, percentage = calculate_poor_bridge_percentage(municipality_bridges)
        print(f"{municipality}: Total: {total}, Poor: {poor}, Percentage: {percentage:.2f}%")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_bridges(json_file_path)
