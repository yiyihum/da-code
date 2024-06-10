import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
nobel_df = pd.read_csv('/workspace/nobel.csv')

# Extract the decade from the year
nobel_df['Decade'] = (nobel_df['year'] // 10) * 10

# Find the most common birth country
most_common_birth_country = nobel_df['birth_country'].mode()[0]

# Calculate the proportion of Nobel Prize winners born in the most common birth country by decade
proportion_by_decade = nobel_df[nobel_df['birth_country'] == most_common_birth_country].groupby('Decade').size() / nobel_df.groupby('Decade').size()

# Create a line plot
plt.figure(figsize=(10, 5))
proportion_by_decade.plot(kind='line')
plt.title('Proportion of Nobel Prize Winners Born in the most common birth country of Nobel laureates by Decade')
plt.xlabel('Decade')
plt.ylabel('Proportion of USA-born Winners')  # Assuming the most common birth country is the USA
plt.savefig('/workspace/result.jpg')
