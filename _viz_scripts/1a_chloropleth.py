import json
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os
import zipfile

def create_choropleth_map(json_file, shapefile_zip):
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create output folder
    output_dir = os.path.join(script_dir, '1a_output')
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

    # Extract the shapefile from the zip
    with zipfile.ZipFile(shapefile_zip, 'r') as zip_ref:
        zip_ref.extractall(os.path.dirname(shapefile_zip))

    # Load the shapefile
    shapefile_path = shapefile_zip.replace('.zip', '')
    ny_counties = gpd.read_file(shapefile_path)

    # Merge shapefile with our data
    ny_counties['NAME'] = ny_counties['NAME'].str.upper()
    merged = ny_counties.merge(county_data, left_on='NAME', right_on='County', how='left')

    # Create the plot
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    merged.plot(column='Poor Percentage', ax=ax, legend=True, 
                legend_kwds={'label': 'Percentage of Poor Condition Bridges'},
                cmap='YlOrRd', missing_kwds={'color': 'lightgrey'})

    # Customize the plot
    ax.set_title('Percentage of Poor Condition Bridges by County in New York State', fontsize=16)
    ax.axis('off')

    # Save the plot
    output_path = os.path.join(output_dir, 'ny_bridge_condition_choropleth.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Choropleth map saved as: {output_path}")

# Run the function
if __name__ == "__main__":
    json_file = 'bridge_conditions.json'
    shapefile_zip = 'references/NYS_Civil_Boundaries.shp.zip'
    create_choropleth_map(json_file, shapefile_zip)
