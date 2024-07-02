import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon
import numpy as np
from scipy import stats
import os

def perform_spatial_analysis():
    # Create 3d_data folder if it doesn't exist
    if not os.path.exists('3d_data'):
        os.makedirs('3d_data')

    # Load the merged data
    merged_gdf = gpd.read_file('3b_data/merged_bridge_data.geojson')

    # Create a point pattern of poor condition bridges
    poor_bridges = merged_gdf[merged_gdf['Poor Status'] == 'Y']
    poor_bridges_points = np.array([(point.x, point.y) for point in poor_bridges.geometry])

    # Perform kernel density estimation
    x, y = poor_bridges_points.T
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    positions = np.vstack([X.ravel(), Y.ravel()])
    values = np.vstack([x, y])
    kernel = stats.gaussian_kde(values)
    Z = np.reshape(kernel(positions).T, X.shape)

    # Create a simplified New York State boundary
    ny_boundary = Polygon([
        (xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)
    ])
    ny_gdf = gpd.GeoDataFrame(geometry=[ny_boundary], crs=merged_gdf.crs)

    # Plot the kernel density
    fig, ax = plt.subplots(figsize=(12, 8))
    im = ax.imshow(np.rot90(Z), cmap=plt.cm.viridis, extent=[xmin, xmax, ymin, ymax])
    ax.plot(x, y, 'r.', markersize=2, alpha=0.5)
    ax.set_title('Kernel Density of Poor Condition Bridges in New York State')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    plt.colorbar(im, ax=ax, label='Density')
    
    # Add simplified New York state boundary
    ny_gdf.boundary.plot(ax=ax, color='black', linewidth=1)

    plt.tight_layout()
    plt.savefig('3d_data/poor_bridges_density.png', dpi=300)
    plt.close()

    print("Spatial analysis results saved in the '3d_data' folder.")

if __name__ == "__main__":
    perform_spatial_analysis()
