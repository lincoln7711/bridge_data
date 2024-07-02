import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from pointpats import PointPattern, KernelDensity
import os

def perform_spatial_analysis():
    # Create 3d_data folder if it doesn't exist
    if not os.path.exists('3d_data'):
        os.makedirs('3d_data')

    # Load the merged data
    merged_gdf = gpd.read_file('3b_data/merged_bridge_data.geojson')

    # Create a point pattern of poor condition bridges
    poor_bridges = merged_gdf[merged_gdf['Poor Status'] == 'Y']
    poor_bridges_points = [Point(xy) for xy in zip(poor_bridges.geometry.x, poor_bridges.geometry.y)]

    # Perform kernel density estimation
    pp = PointPattern(poor_bridges_points)
    kde = KernelDensity(pp)

    # Plot the kernel density
    fig, ax = plt.subplots(figsize=(12, 8))
    kde.plot(ax=ax)
    ax.set_title('Kernel Density of Poor Condition Bridges')
    plt.savefig('3d_data/poor_bridges_density.png')

    print("Spatial analysis results saved in the '3d_data' folder.")

if __name__ == "__main__":
    perform_spatial_analysis()
