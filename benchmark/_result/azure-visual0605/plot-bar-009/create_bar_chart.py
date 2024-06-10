import pandas as pd
import matplotlib.pyplot as plt

# Load the Coaches data
coaches_df = pd.read_excel('/workspace/Coaches.xlsx')
# Count the number of coaches per country
coaches_count = coaches_df['NOC'].value_counts()

# Load the Medals data
medals_df = pd.read_excel('/workspace/Medals.xlsx')
# Count the number of gold medals per country
gold_medals_count = medals_df.set_index('Team/NOC')['Gold']

# Combine the data into a single DataFrame
combined_df = pd.DataFrame({
    'Coaches': coaches_count,
    'Gold Medals': gold_medals_count
}).fillna(0)  # Fill NaN values with 0

# Sort by the number of coaches in descending order and take the top 10
top_countries = combined_df.sort_values(by='Coaches', ascending=False).head(10)

# Plotting the bar chart
fig, ax = plt.subplots(figsize=(12, 6))
top_countries.plot(kind='bar', ax=ax)
ax.set_title('Number of Coaches and Gold Medals by Country')
ax.set_xlabel('Countries')
ax.set_ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the bar chart as 'result.png'
plt.savefig('/workspace/result.png')
