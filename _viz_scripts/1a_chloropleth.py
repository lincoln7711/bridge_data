import json
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os

def create_choropleth_map(json_file, shapefile_path):
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create 1a_output folder
    output_dir = os.path.join(script_dir, '1a_output')
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

    # Group by county and calculate poor bridge percentage
    county_data = df.groupby('County').agg({
        'BIN': 'count',
        'Poor Status': lambda x: (x == 'Y').sum()
    }).reset_index()
    county_data['Poor Percentage'] = (county_data['Poor Status'] / county_data['BIN']) * 100

    # Load the shapefile
    print(f"Loading shapefile: {shapefile_path}")
    ny_counties = gpd.read_file(shapefile_path)

    # Merge shapefile with our data
    merged = ny_counties.merge(county_data, left_on='NAME', right_on='County', how='left')

    # Create a new column with county name and percentage
    merged['County_Percentage'] = merged['NAME'] + ' (' + merged['Poor Percentage'].round(2).astype(str) + '%)'

    # Create the plot
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged.plot(column='Poor Percentage', ax=ax, legend=True, 
                legend_kwds={'label': 'Percentage of Poor Condition Bridges'},
                cmap='YlOrRd', missing_kwds={'color': 'lightgrey'})

    # Add labels with county name and percentage
    for idx, row in merged.iterrows():
        ax.annotate(row['County_Percentage'], xy=(row['geometry'].centroid.x, row['geometry'].centroid.y),
                    xytext=(3, 3), textcoords="offset points", fontsize=6, ha='center', va='center')

    # Customize the plot
    ax.set_title('Percentage of Poor Condition Bridges by County in New York State', fontsize=16)
    ax.axis('off')

    # Save the plot with a new filename
    output_path = os.path.join(output_dir, 'ny_bridge_condition_choropleth_with_percentages.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Choropleth map saved as: {output_path}")

# Run the function
if __name__ == "__main__":
    json_file = 'bridge_conditions.json'
    shapefile_path = '/Users/andrewsmith/Documents/GitHub/bridge_data/_viz_scripts/references/Counties.shp'
    create_choropleth_map(json_file, shapefile_path)
