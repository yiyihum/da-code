import pandas as pd

# Load the Coaches data
coaches_df = pd.read_excel('/workspace/Coaches.xlsx')
# Count the number of coaches per country
coaches_count = coaches_df['NOC'].value_counts()

# Load the Medals data
medals_df = pd.read_excel('/workspace/Medals.xlsx')
# Count the number of gold medals per country
gold_medals_count = medals_df[medals_df['Medal'] == 'Gold']['NOC'].value_counts()

# Combine the data into a single DataFrame
combined_df = pd.DataFrame({
    'Coaches': coaches_count,
    'Gold Medals': gold_medals_count
}).fillna(0)  # Fill NaN values with 0

# Sort by the number of coaches in descending order and take the top 10
top_countries = combined_df.sort_values(by='Coaches', ascending=False).head(10)

# Save the top countries DataFrame to a CSV for further inspection
top_countries.to_csv('/workspace/top_countries.csv', index=True)
print(top_countries)
