import pandas as pd
import matplotlib.pyplot as plt
import os

def create_stacked_bar_chart(csv_file):
    # Create output folder in the main repository
    if not os.path.exists('../1c_output'):
        os.makedirs('../1c_output')

    # Read the CSV file from the main repository
    df = pd.read_csv(os.path.join('..', csv_file))

    # Group by county and calculate totals
    county_data = df.groupby('County').agg({
        'BIN': 'count',
        'Poor Status': lambda x: (x == 'Y').sum()
    }).reset_index()
    county_data['Good Condition'] = county_data['BIN'] - county_data['Poor Status']

    # Sort by total number of bridges
    county_data = county_data.sort_values('BIN', ascending=False)

    # Create the stacked bar chart
    plt.figure(figsize=(15, 10))
    plt.bar(county_data['County'], county_data['Good Condition'], label='Good Condition')
    plt.bar(county_data['County'], county_data['Poor Status'], bottom=county_data['Good Condition'], label='Poor Condition')

    # Customize the plot
    plt.xlabel('County', fontsize=12)
    plt.ylabel('Number of Bridges', fontsize=12)
    plt.title('Bridge Conditions by County in New York State', fontsize=16)
    plt.legend(loc='upper right')
    plt.xticks(rotation=90, ha='right')

    # Adjust layout and save in the main repository
    plt.tight_layout()
    plt.savefig('../1c_output/bridge_condition_stacked_bar.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("Stacked bar chart saved in 1c_output folder in the main repository.")

# Run the function
if __name__ == "__main__":
    create_stacked_bar_chart('Bridge_Conditions__NYS_Department_of_Transportation_20240702.csv')
