import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('nobel.csv')

# Add a decade column
df['decade'] = (df['year'] // 10) * 10

# Group by decade, category, and sex, and count the number of laureates
grouped = df.groupby(['decade', 'category', 'sex']).size().reset_index(name='count')

# Find the gender with the most laureates for each decade and category
top_gender = grouped.loc[grouped.groupby(['decade', 'category'])['count'].idxmax()]

# Merge to get the total count for each decade and category
total_counts = df.groupby(['decade', 'category']).size().reset_index(name='total_count')
merged = pd.merge(top_gender, total_counts, on=['decade', 'category'])

# Calculate the percentage
merged['percentage'] = (merged['count'] / merged['total_count']) * 100

# Plot the results
plt.figure(figsize=(10, 6))
for category in merged['category'].unique():
    subset = merged[merged['category'] == category]
    plt.plot(subset['decade'], subset['percentage'], marker='o', label=category)

plt.title('Proportion of Top Gender Nobel Prize Winners by Decade and Category')
plt.xlabel('Decade')
plt.ylabel('Percentage of Top Gender Winners')
plt.legend(title='Category')
plt.grid(True)
plt.savefig('result.jpg')
plt.close()
