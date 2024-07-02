import json
import pandas as pd
import matplotlib.pyplot as plt
import os

def create_stacked_bar_chart(json_file):
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create output folder
    output_dir = os.path.join(script_dir, '1c_output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Construct the full path to the JSON file
    json_path = os.path.join(script_dir, 'references', json_file)

    # Read the JSON file
    print(f"Reading JSON file: {json_path}")
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Group by county and calculate totals
    county_data = df.groupby('County').agg({
        'BIN': 'count',
        'Poor Status': lambda x: (x == 'Y').sum()
    }).reset_index()
    county_data['Good Condition'] = county_data['BIN'] - county_data['Poor Status']

    # Sort by total number of bridges
    county_data = county_data.sort_values('BIN', ascending=False)

    # Create the stacked bar chart
    plt.figure(figsize=(15, 10))
    plt.bar(county_data['County'], county_data['Good Condition'], label='Good Condition')
    plt.bar(county_data['County'], county_data['Poor Status'], bottom=county_data['Good Condition'], label='Poor Condition')

    # Customize the plot
    plt.xlabel('County', fontsize=12)
    plt.ylabel('Number of Bridges', fontsize=12)
    plt.title('Bridge Conditions by County in New York State', fontsize=16)
    plt.legend(loc='upper right')
    plt.xticks(rotation=90, ha='right')

    # Adjust layout and save
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'bridge_condition_stacked_bar.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Stacked bar chart saved as: {output_path}")

# Run the function
if __name__ == "__main__":
    create_stacked_bar_chart('bridge_conditions.json')
