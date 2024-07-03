import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('bridges_by_decade.txt', sep=':', header=None, names=['Decade', 'Data'])
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
plt.show()