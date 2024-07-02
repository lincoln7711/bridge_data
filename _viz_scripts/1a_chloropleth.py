import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
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

def create_choropleth_map(csv_file):
    # Create output folder in the main repository
    if not os.path.exists('../1a_output'):
        os.makedirs('../1a_output')

    # Read the CSV file
    print(f"Reading CSV file from: {csv_file}")
    df = pd.read_csv(csv_file)

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

    # Save the plot in the main repository
    output_path = os.path.join('..', '1a_output', 'ny_bridge_condition_choropleth.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Choropleth map saved as: {output_path}")

# Run the function
if __name__ == "__main__":
    create_choropleth_map('Bridge_Conditions__NYS_Department_of_Transportation_20240702.csv')
