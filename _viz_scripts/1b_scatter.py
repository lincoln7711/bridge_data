import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def create_scatter_plot(json_file):
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create output folder
    output_dir = os.path.join(script_dir, '1b_output')
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

    # Create the scatter plot
    plt.figure(figsize=(12, 8))
    plt.scatter(county_data['BIN'], county_data['Poor Status'], alpha=0.6)

    # Customize the plot
    plt.xlabel('Total Number of Bridges', fontsize=12)
    plt.ylabel('Number of Poor Condition Bridges', fontsize=12)
    plt.title('Total Bridges vs Poor Condition Bridges by County', fontsize=16)

    # Add county labels to points
    for i, txt in enumerate(county_data['County']):
        plt.annotate(txt, (county_data['BIN'][i], county_data['Poor Status'][i]), fontsize=8)

    # Add a trend line
    z = np.polyfit(county_data['BIN'], county_data['Poor Status'], 1)
    p = np.poly1d(z)
    plt.plot(county_data['BIN'], p(county_data['BIN']), "r--", alpha=0.8)

    # Save the plot
    output_path = os.path.join(output_dir, 'bridge_condition_scatter_plot.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Scatter plot saved as: {output_path}")

# Run the function
if __name__ == "__main__":
    create_scatter_plot('bridge_conditions.json')
