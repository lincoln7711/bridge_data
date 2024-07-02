import geopandas as gpd
import folium
from folium.plugins import MarkerCluster, HeatMap
import os

def create_interactive_map():
    # Create 3c_data folder if it doesn't exist
    if not os.path.exists('3c_data'):
        os.makedirs('3c_data')

    # Load the merged data
    merged_gdf = gpd.read_file('3b_data/merged_bridge_data.geojson')

    # Create a base map centered on New York State
    m = folium.Map(location=[42.9538, -75.5268], zoom_start=7)

    # Create a marker cluster
    marker_cluster = MarkerCluster().add_to(m)

    # Add points for all bridges
    for idx, row in merged_gdf.iterrows():
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=5,
            popup=f"BIN: {row.BIN}, Condition: {'Poor' if row['Poor Status'] == 'Y' else 'Not Poor'}",
            color='red' if row['Poor Status'] == 'Y' else 'blue',
            fill=True
        ).add_to(marker_cluster)

    # Create a heatmap of poor condition bridges
    poor_bridges = merged_gdf[merged_gdf['Poor Status'] == 'Y']
    HeatMap(data=poor_bridges[['geometry.y', 'geometry.x']], radius=15).add_to(m)

    # Save the map
    m.save('3c_data/bridge_condition_map.html')

    print("Interactive map saved in the '3c_data' folder.")

if __name__ == "__main__":
    create_interactive_map()
