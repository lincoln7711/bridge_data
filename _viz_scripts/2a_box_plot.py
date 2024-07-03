import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set up file paths
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_file = os.path.join(project_dir, '2_data', 'bridges_by_decade.txt')
output_dir = os.path.join(project_dir, '2a_output')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Load the data
df = pd.read_csv(data_file, sep=':', header=None, names=['Decade', 'Data'])
df[['Total', 'Poor', 'Percentage']] = df['Data'].str.extract(r'Total: (\d+), Poor: (\d+), Percentage: ([\d.]+)%')
df = df.drop('Data', axis=1)
df[['Total', 'Poor', 'Percentage']] = df[['Total', 'Poor', 'Percentage']].astype(float)

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

print(f"Box plot saved to {output_file}")