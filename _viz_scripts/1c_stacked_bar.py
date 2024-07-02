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
    county_data['Good Ratio'] = county_data['Good Condition'] / county_data['BIN']

    # Sort by total number of bridges
    county_data = county_data.sort_values('BIN', ascending=False)

    # Create the stacked bar chart
    fig, ax = plt.subplots(figsize=(15, 10))
    bars_good = ax.bar(county_data['County'], county_data['Good Condition'], label='Good Condition')
    bars_poor = ax.bar(county_data['County'], county_data['Poor Status'], bottom=county_data['Good Condition'], label='Poor Condition')

    # Customize the plot
    ax.set_xlabel('County', fontsize=12)
    ax.set_ylabel('Number of Bridges', fontsize=12)
    ax.set_title('Bridge Conditions by County in New York State', fontsize=16)
    plt.xticks(rotation=90, ha='right')

    # Create legend with good condition ratios
    legend_labels = [f"{county}: {good_ratio:.2f}" for county, good_ratio in zip(county_data['County'], county_data['Good Ratio'])]
    ax.legend(bars_good, legend_labels, title='Good Condition Ratio', loc='upper right', bbox_to_anchor=(1.25, 1), fontsize=8)

    # Adjust layout and save
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'bridge_condition_stacked_bar_with_legend.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Stacked bar chart saved as: {output_path}")

# Run the function
if __name__ == "__main__":
    create_stacked_bar_chart('bridge_conditions.json')
