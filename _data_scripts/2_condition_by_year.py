import json
import os
from collections import defaultdict

def calculate_poor_bridge_percentage(bridges):
    total_bridges = len(bridges)
    poor_bridges = sum(1 for bridge in bridges if bridge['Poor Status'] == 'Y')
    poor_percentage = (poor_bridges / total_bridges) * 100 if total_bridges > 0 else 0
    return total_bridges, poor_bridges, poor_percentage

def analyze_bridges_by_year(json_file_path):
    with open(json_file_path, 'r') as json_file:
        bridges = json.load(json_file)

    # Create 2_data folder if it doesn't exist
    if not os.path.exists('2_data'):
        os.makedirs('2_data')

    # Group bridges by year
    bridges_by_year = defaultdict(list)
    for bridge in bridges:
        year = bridge['Year Built or Replaced']
        if year.isdigit():
            bridges_by_year[int(year)].append(bridge)

    # Analyze by individual year
    with open('2_data/bridges_by_year.txt', 'w') as f:
        f.write("Bridges by Year Built/Replaced:\n")
        for year in sorted(bridges_by_year.keys()):
            total, poor, percentage = calculate_poor_bridge_percentage(bridges_by_year[year])
            f.write(f"{year}: Total: {total}, Poor: {poor}, Percentage: {percentage:.2f}%\n")

    # Analyze by 5-year periods
    five_year_periods = defaultdict(list)
    for year, year_bridges in bridges_by_year.items():
        period = (year // 5) * 5
        five_year_periods[period].extend(year_bridges)

    with open('2_data/bridges_by_5_year_period.txt', 'w') as f:
        f.write("Bridges by 5-Year Periods:\n")
        for period in sorted(five_year_periods.keys()):
            total, poor, percentage = calculate_poor_bridge_percentage(five_year_periods[period])
            f.write(f"{period}-{period+4}: Total: {total}, Poor: {poor}, Percentage: {percentage:.2f}%\n")

    # Analyze by decade
    decades = defaultdict(list)
    for year, year_bridges in bridges_by_year.items():
        decade = (year // 10) * 10
        decades[decade].extend(year_bridges)

    with open('2_data/bridges_by_decade.txt', 'w') as f:
        f.write("Bridges by Decade:\n")
        for decade in sorted(decades.keys()):
            total, poor, percentage = calculate_poor_bridge_percentage(decades[decade])
            f.write(f"{decade}s: Total: {total}, Poor: {poor}, Percentage: {percentage:.2f}%\n")

    print("Analysis complete. Results saved in the '2_data' folder.")

# Usage
json_file_path = 'bridge_conditions.json'
analyze_bridges_by_year(json_file_path)
