import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def create_scatter_plot(csv_file):
    # Create output folder in the main repository
    if not os.path.exists('../1b_output'):
        os.makedirs('../1b_output')

    # Read the CSV file from the main repository
    df = pd.read_csv(os.path.join('..', csv_file))

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

    # Save the plot in the main repository
    plt.savefig('../1b_output/bridge_condition_scatter_plot.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("Scatter plot saved in 1b_output folder in the main repository.")

# Run the function
if __name__ == "__main__":
    create_scatter_plot('Bridge_Conditions__NYS_Department_of_Transportation_20240702.csv')
