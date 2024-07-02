import pandas as pd
import geopandas as gpd
import os

def merge_geojson_with_condition_data():
    # Create 3b_data folder if it doesn't exist
    if not os.path.exists('3b_data'):
        os.makedirs('3b_data')

    # Load the GeoJSON data
    gdf = gpd.read_file('3a_data/nysdot_bridges.geojson')

    # Load the bridge condition data
    condition_df = pd.read_csv('Bridge_Conditions__NYS_Department_of_Transportation_20240702.csv')

    # Merge the GeoJSON data with the condition data
    merged_gdf = gdf.merge(condition_df, left_on='BIN', right_on='BIN', how='inner')

    # Save the merged data
    merged_gdf.to_file('3b_data/merged_bridge_data.geojson', driver='GeoJSON')

    print("Merged data saved in the '3b_data' folder.")

if __name__ == "__main__":
    merge_geojson_with_condition_data()
