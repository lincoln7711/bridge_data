import json
import os
from datetime import datetime, timedelta

def analyze_inspection_dates(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 4b_data folder if it doesn't exist
    if not os.path.exists('4b_data'):
        os.makedirs('4b_data')

    # Set the reference date (Data Last Updated February 20, 2020)
    reference_date = datetime(2020, 2, 20)

    # Thresholds
    threshold_24_months = timedelta(days=730)  # 24 months
    threshold_48_months = timedelta(days=1460)  # 48 months

    results = []
    poor_condition_results = []

    for bridge in bridges:
        try:
            inspection_date = datetime.strptime(bridge['Date of Last Inspection'], '%m/%d/%Y')
            time_since_inspection = reference_date - inspection_date
            
            is_overdue_24 = time_since_inspection > threshold_24_months
            is_overdue_48 = time_since_inspection > threshold_48_months
            is_poor_condition = bridge['Poor Status'] == 'Y'

            result = {
                'BIN': bridge['BIN'],
                'Last Inspection': inspection_date.strftime('%Y-%m-%d'),
                'Days Since Inspection': time_since_inspection.days,
                'Overdue (24 months)': 'Y' if is_overdue_24 else 'N',
                'Overdue (48 months)': 'Y' if is_overdue_48 else 'N',
                'Poor Condition': 'Y' if is_poor_condition else 'N'
            }
            results.append(result)

            if is_poor_condition:
                poor_condition_results.append({
                    'BIN': bridge['BIN'],
                    'Last Inspection': inspection_date.strftime('%Y-%m-%d'),
                    'Days Since Inspection': time_since_inspection.days,
                    'Inspected Within 24 Months': 'Y' if time_since_inspection <= threshold_24_months else 'N'
                })

        except ValueError:
            # Skip invalid date formats
            continue

    # Write results to file
    with open('4b_data/inspection_overdue_analysis.txt', 'w') as f:
        f.write("Bridge Inspection Overdue Analysis:\n")
        f.write("BIN, Last Inspection, Days Since Inspection, Overdue (24 months), Overdue (48 months), Poor Condition\n")
        for result in results:
            f.write(f"{result['BIN']}, {result['Last Inspection']}, {result['Days Since Inspection']}, "
                    f"{result['Overdue (24 months)']}, {result['Overdue (48 months)']}, {result['Poor Condition']}\n")

    # Write poor condition bridge analysis to file
    with open('4b_data/poor_condition_bridge_analysis.txt', 'w') as f:
        f.write("Poor Condition Bridge Inspection Analysis:\n")
        f.write("BIN, Last Inspection, Days Since Inspection, Inspected Within 24 Months\n")
        for result in poor_condition_results:
            f.write(f"{result['BIN']}, {result['Last Inspection']}, {result['Days Since Inspection']}, "
                    f"{result['Inspected Within 24 Months']}\n")

    print("Analysis complete. Results saved in the '4b_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_inspection_dates(json_file_path)
