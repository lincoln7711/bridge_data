import json
import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

def create_choropleth_map(json_file):
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create output folder
    output_dir = os.path.join(script_dir, 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Construct the full path to the JSON file
    json_path = os.path.join(script_dir, json_file)

    # Read the JSON file
    print(f"Reading JSON file: {json_path}")
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {json_path} was not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: The file {json_path} is not a valid JSON file.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Group by county and calculate poor bridge percentage
    county_data = df.groupby('County').agg({
        'BIN': 'count',
        'Poor Status': lambda x: (x == 'Y').sum()
    }).reset_index()
    county_data['Poor Percentage'] = (county_data['Poor Status'] / county_data['BIN']) * 100

    # Create a simplified map
    fig, ax = plt.subplots(figsize=(15, 10))

    # Create dummy polygons for each county
    polygons = []
    for i, county in enumerate(county_data['County']):
        x = i % 8  # 8 columns
        y = i // 8
        poly = Polygon([(x, y), (x+1, y), (x+1, y+1), (x, y+1)])
        polygons.append(poly)

    # Create a PatchCollection with the polygons
    p = PatchCollection(polygons, cmap='YlOrRd')
    p.set_array(county_data['Poor Percentage'])
    ax.add_collection(p)

    # Add county labels
    for i, county in enumerate(county_data['County']):
        x = i % 8 + 0.5
        y = i // 8 + 0.5
        ax.text(x, y, county, ha='center', va='center', fontsize=8)

    # Set the limits and remove axes
    ax.set_xlim(0, 8)
    ax.set_ylim(0, len(county_data) // 8 + 1)
    ax.axis('off')

    # Add a colorbar
    cbar = plt.colorbar(p, ax=ax)
    cbar.set_label('Percentage of Poor Condition Bridges')

    # Set the title
    plt.title('Percentage of Poor Condition Bridges by County in New York State', fontsize=16)

    # Save the plot
    output_path = os.path.join(output_dir, 'ny_bridge_condition_choropleth.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Choropleth map saved as: {output_path}")

# Run the function
if __name__ == "__main__":
    create_choropleth_map('bridge_conditions.json')
