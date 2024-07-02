import json
import os

# Dictionary to categorize owners
owner_categories = {
    'Private': ['Utility', 'Railroad'],
    'Public': [
        'Federal (Other than those listed below)', 'National Park Service',
        'Alleghany State Park Authority', 'Town', 'Village',
        'Niagara Frontier State Park Commission', 'NYS Thruway Authority',
        'NYS Dept of Environmental Conservation', 'NYS Bridge Authority',
        'City', 'County', 'Transit Authority', 'MTA Bridges and Tunnels (aka TBTA)',
        'NYSDOT', 'NYC Dept of Water Supply, Gas and Electric',
        'Metropolitan Transportation Authority', 'Palisades Interstate Park Commission',
        'State - Other', 'City of NY State Park Commission', 'Other',
        'Finger Lakes Parks and Recreation Commission', 'Authority or Commission - Other',
        'Peace Bridge Authority (aka Buffalo And Ft. Erie Pub Br.Auth)',
        'Thousand Islands Bridge Authority', 'Genesee State Parks and Recreation Commission',
        'Nassau County Bridge Authority', 'Port Authority of NY and NJ',
        'NYS Power Authority', 'Niagara Falls Bridge Commission',
        'Central NY State Park Commission', 'Seaway International Bridge Authority',
        'Ogdensburg Bridge and Port Authority'
    ]
}

def categorize_owner(owner):
    for category, owners in owner_categories.items():
        if owner in owners:
            return category
    return 'Unknown'  # For any owner not explicitly categorized

def analyze_public_private_bridges(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 5c_data folder if it doesn't exist
    if not os.path.exists('5c_data'):
        os.makedirs('5c_data')

    # Dictionary to store bridge counts
    bridge_counts = {
        'Public': {'total': 0, 'poor': 0},
        'Private': {'total': 0, 'poor': 0},
        'Unknown': {'total': 0, 'poor': 0}
    }

    # Dictionary to store individual owner data
    owner_data = {}

    for bridge in bridges:
        owner = bridge['Owner']
        owner_type = categorize_owner(owner)
        
        # Update overall counts
        bridge_counts[owner_type]['total'] += 1
        if bridge['Poor Status'] == 'Y':
            bridge_counts[owner_type]['poor'] += 1
        
        # Update individual owner data
        if owner not in owner_data:
            owner_data[owner] = {'type': owner_type, 'total': 0, 'poor': 0}
        owner_data[owner]['total'] += 1
        if bridge['Poor Status'] == 'Y':
            owner_data[owner]['poor'] += 1

    # Calculate percentages and prepare results
    results = []
    for owner_type, counts in bridge_counts.items():
        poor_percentage = (counts['poor'] / counts['total']) * 100 if counts['total'] > 0 else 0
        results.append({
            'Owner Type': owner_type,
            'Total Bridges': counts['total'],
            'Poor Condition Bridges': counts['poor'],
            'Poor Percentage': poor_percentage
        })

    # Write overall results to file
    with open('5c_data/public_private_bridge_analysis.txt', 'w') as f:
        f.write("Public vs Private Bridge Ownership Analysis:\n")
        f.write("Owner Type, Total Bridges, Poor Condition Bridges, Poor %\n")
        for result in results:
            f.write(f"{result['Owner Type']}, {result['Total Bridges']}, {result['Poor Condition Bridges']}, "
                    f"{result['Poor Percentage']:.2f}%\n")

    # Write individual owner data to file
    with open('5c_data/individual_owner_analysis.txt', 'w') as f:
        f.write("Individual Owner Analysis:\n")
        f.write("Owner, Type, Total Bridges, Poor Condition Bridges, Poor %\n")
        for owner, data in owner_data.items():
            poor_percentage = (data['poor'] / data['total']) * 100 if data['total'] > 0 else 0
            f.write(f"{owner}, {data['type']}, {data['total']}, {data['poor']}, {poor_percentage:.2f}%\n")

    print("Analysis complete. Results saved in the '5c_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_public_private_bridges(json_file_path)
