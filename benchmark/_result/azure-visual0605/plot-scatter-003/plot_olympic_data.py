import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/athlete_events.csv')

# Group by 'Year' and count the number of unique athletes
athletes_per_year = df.groupby('Year')['ID'].nunique().reset_index()

# Plotting
plt.figure(figsize=(12, 8))
plt.scatter(athletes_per_year['Year'], athletes_per_year['ID'], color='blue')
plt.title('Athletes per Olympic game')
plt.xlabel('Year')
plt.ylabel('Number of athletes')
plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000], ['0', '2k', '4k', '6k', '8k', '10k', '12k'])

# Save the plot
plt.savefig('/workspace/result.png')
