import json
import pandas as pd
import matplotlib.pyplot as plt
import os

def create_stacked_bar_chart_with_table(json_file):
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

    # Create the figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10), gridspec_kw={'width_ratios': [3, 1]})

    # Create the stacked bar chart
    bars_good = ax1.bar(county_data['County'], county_data['Good Condition'], label='Good Condition')
    bars_poor = ax1.bar(county_data['County'], county_data['Poor Status'], bottom=county_data['Good Condition'], label='Poor Condition')

    # Customize the plot
    ax1.set_xlabel('County', fontsize=12)
    ax1.set_ylabel('Number of Bridges', fontsize=12)
    ax1.set_title('Bridge Conditions by County in New York State', fontsize=16)
    ax1.legend(loc='upper right')
    plt.setp(ax1.get_xticklabels(), rotation=90, ha='right')

    # Create the table with good condition ratios
    table_data = county_data[['County', 'Good Condition', 'BIN']].copy()
    table_data['Ratio'] = table_data.apply(lambda row: f"{row['Good Condition']}/{row['BIN']}", axis=1)
    table_data = table_data[['County', 'Ratio']]

    ax2.axis('off')
    table = ax2.table(cellText=table_data.values, colLabels=table_data.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)
    ax2.set_title('Ratio of Bridges in Good Condition', fontsize=14)

    # Adjust layout and save
    plt.tight_layout()
    output_path = os.path.join(output_dir, 'bridge_condition_stacked_bar_with_table.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Stacked bar chart with table saved as: {output_path}")

# Run the function
if __name__ == "__main__":
    create_stacked_bar_chart_with_table('bridge_conditions.json')
