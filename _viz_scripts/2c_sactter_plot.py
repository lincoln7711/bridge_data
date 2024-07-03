import os
import pandas as pd
import matplotlib.pyplot as plt

# Set up file paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
data_file = os.path.join(project_dir, '2_data', 'bridges_by_decade.txt')
output_dir = os.path.join(current_dir, '2c_output')

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

# Convert decade to numeric for plotting
df['Decade_Num'] = pd.to_numeric(df['Decade'].str[:4])

# Create the scatter plot
plt.figure(figsize=(12, 6))
scatter = plt.scatter(df['Decade_Num'], df['Percentage'], s=df['Total']/10, alpha=0.6)

plt.title('Percentage of Poor Bridges by Decade')
plt.xlabel('Decade')
plt.ylabel('Percentage of Poor Bridges')
plt.ylim(0, max(df['Percentage']) * 1.1)  # Set y-axis limit with some padding

# Customize x-axis ticks
plt.xticks(df['Decade_Num'], df['Decade'], rotation=45, ha='right')

# Add labels for each point
for i, row in df.iterrows():
    plt.annotate(f"{row['Percentage']:.2f}%", 
                 (row['Decade_Num'], row['Percentage']),
                 xytext=(5, 5), textcoords='offset points', fontsize=8)

# Add a legend for bubble size
legend_sizes = [100, 1000, 2000]
legend_labels = ['100', '1000', '2000']
legend_bubbles = []
for size in legend_sizes:
    legend_bubbles.append(plt.scatter([], [], s=size/10, c='gray', alpha=0.6))

plt.legend(legend_bubbles, legend_labels, scatterpoints=1, labelspacing=1.5,
           title='Total Bridges', loc='upper left', bbox_to_anchor=(1, 1))

plt.tight_layout()

# Save the plot
output_file = os.path.join(output_dir, 'scatter_plot_poor_bridges_by_decade.png')
plt.savefig(output_file, bbox_inches='tight')
plt.close()

print(f"Scatter plot saved to {output_file}")