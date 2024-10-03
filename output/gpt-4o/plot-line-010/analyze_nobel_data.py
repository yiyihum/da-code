import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('nobel.csv')

# Extract the decade from the year
df['decade'] = (df['year'] // 10) * 10

# Group by decade and birth country, and count the number of winners
country_counts = df.groupby(['decade', 'birth_country']).size().reset_index(name='count')

# Find the most common birth country for each decade
most_common_countries = country_counts.loc[country_counts.groupby('decade')['count'].idxmax()]

# Merge with the original data to calculate the proportion
merged = pd.merge(df, most_common_countries[['decade', 'birth_country']], on=['decade', 'birth_country'], how='inner')

# Calculate the proportion of winners from the most common birth country for each decade
proportion = merged.groupby('decade').size() / df.groupby('decade').size()

# Plot the results
plt.figure(figsize=(10, 5))
plt.plot(proportion.index, proportion.values, marker='o')
plt.title('Proportion of Nobel Prize Winners Born in the most common birth country of Nobel laureates by Decade')
plt.xlabel('Decade')
plt.ylabel('Proportion of USA-born Winners')
plt.grid(True)
plt.savefig('result.jpg')
plt.close()
