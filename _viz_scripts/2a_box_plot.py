import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set up file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
data_file = os.path.join(project_dir, '2_data', 'bridges_by_decade.txt')
output_dir = os.path.join(current_dir, '2a_output')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read the file content
with open(data_file, 'r') as file:
    lines = file.readlines()

# Print the first few lines of the file
print("First few lines of the file:")
for line in lines[:5]:
    print(line.strip())

# Process the data
data = []
for line in lines[1:]:  # Skip the header line
    parts = line.strip().split(':')
    if len(parts) == 2:
        decade = parts[0].strip()
        values = parts[1].strip().split(',')
        if len(values) == 3:
            total = int(values[0].split(':')[1].strip())
            poor = int(values[1].split(':')[1].strip())
            percentage = float(values[2].split(':')[1].strip().rstrip('%'))
            data.append({'Decade': decade, 'Total': total, 'Poor': poor, 'Percentage': percentage})

# Create DataFrame
df = pd.DataFrame(data)

# Print the DataFrame
print("\nDataFrame contents:")
print(df)

# Check if 'Decade' and 'Percentage' columns exist
if 'Decade' not in df.columns or 'Percentage' not in df.columns:
    print("\nError: 'Decade' or 'Percentage' column is missing from the DataFrame.")
    print("Available columns:", df.columns.tolist())
else:
    # Create the box plot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='Decade', y='Percentage', data=df)
    plt.title('Distribution of Poor Bridge Percentages by Decade')
    plt.xlabel('Decade')
    plt.ylabel('Percentage of Poor Bridges')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot
    output_file = os.path.join(output_dir, 'box_plot_poor_bridges_by_decade.png')
    plt.savefig(output_file)
    plt.close()

    print(f"\nBox plot saved to {output_file}")