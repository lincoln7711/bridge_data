import json
import pandas as pd
import os

def create_bridge_condition_table(json_file):
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create output folder
    output_dir = os.path.join(script_dir, '1c_output')
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

    # Group by county and calculate totals
    county_data = df.groupby('County').agg({
        'BIN': 'count',
        'Poor Status': lambda x: (x == 'Y').sum()
    }).reset_index()
    
    # Calculate good condition bridges and percentages
    county_data['Good Condition'] = county_data['BIN'] - county_data['Poor Status']
    county_data['Good Percentage'] = (county_data['Good Condition'] / county_data['BIN'] * 100).round(2)
    county_data['Poor Percentage'] = (county_data['Poor Status'] / county_data['BIN'] * 100).round(2)

    # Sort by total number of bridges
    county_data = county_data.sort_values('BIN', ascending=False)

    # Rename columns for clarity
    county_data = county_data.rename(columns={
        'BIN': 'Total Bridges',
        'Poor Status': 'Poor Condition',
        'Good Percentage': 'Good Condition %',
        'Poor Percentage': 'Poor Condition %'
    })

    # Reorder columns
    column_order = ['County', 'Total Bridges', 'Good Condition', 'Poor Condition', 
                    'Good Condition %', 'Poor Condition %']
    county_data = county_data[column_order]

    # Save the table as a CSV file
    output_path = os.path.join(output_dir, 'bridge_condition_table.csv')
    county_data.to_csv(output_path, index=False)

    print(f"Bridge condition table saved as: {output_path}")

    # Display the table in the console
    print("\nBridge Condition Table:")
    print(county_data.to_string(index=False))

# Run the function
if __name__ == "__main__":
    create_bridge_condition_table('bridge_conditions.json')
