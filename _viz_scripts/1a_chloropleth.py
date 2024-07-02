import json
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import os
import requests
import zipfile
import io

def download_ny_counties_shapefile():
    url = "https://www2.census.gov/geo/tiger/TIGER2019/COUNTY/tl_2019_36_county.zip"
    response = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(response.content))
    z.extractall("ny_counties_shapefile")
    return gpd.read_file("ny_counties_shapefile/tl_2019_36_county.shp")

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

    # Download and load New York county shapefile
    print("Downloading New York county shapefile...")
    ny_counties = download_ny_counties_shapefile()

    # Merge shapefile with our data
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
    create_choropleth_map('bridge_conditions.json')