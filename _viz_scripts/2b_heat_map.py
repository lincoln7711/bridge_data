import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set up file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
data_file = os.path.join(project_dir, '2_data', 'bridges_by_decade.txt')
output_dir = os.path.join(current_dir, '2b_output')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Read the file content
with open(data_file, 'r') as file:
    lines = file.readlines()

# Process the data
data = []
for line in lines[1:]:  # Skip the header line
    parts = line.strip().split(':')
    if len(parts) >= 2:
        decade = parts[0].strip()
        values = ':'.join(parts[1:]).strip().split(',')
        if len(values) == 3:
            total = int(values[0].split(':')[1].strip())
            poor = int(values[1].split(':')[1].strip())
            percentage = float(values[2].split(':')[1].strip().rstrip('%'))
            data.append({'Decade': decade, 'Total': total, 'Poor': poor, 'Percentage': percentage})

# Create DataFrame
df = pd.DataFrame(data)

# Create the heat map
plt.figure(figsize=(12, 8))
sns.heatmap(df.set_index('Decade')[['Percentage']], cmap='YlOrRd', annot=True, fmt='.2f')
plt.title('Percentage of Poor Bridges by Decade')
plt.ylabel('Decade')
plt.xlabel('')
plt.tight_layout()

# Save the plot
output_file = os.path.join(output_dir, 'heatmap_poor_bridges_by_decade.png')
plt.savefig(output_file)
plt.close()

print(f"Heat map saved to {output_file}")