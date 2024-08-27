import pandas as pd

# Load the fully merged data
merged_all_df = pd.read_csv('/workspace/merged_all_data.csv')

# Find the oldest business year for each continent
oldest_year_per_continent = merged_all_df.groupby('continent')['year_founded'].min().reset_index()

# Merge to filter the oldest businesses on each continent
oldest_businesses = pd.merge(merged_all_df, oldest_year_per_continent, on=['continent', 'year_founded'])

# Group by continent and industry, and count the number of businesses
industry_counts = oldest_businesses.groupby(['continent', 'industry']).size().reset_index(name='count')

# Filter out the industries with a count greater than 5
popular_industries = industry_counts[industry_counts['count'] > 5]

# Sort the results by continent and count in descending order
popular_industries_sorted = popular_industries.sort_values(by=['continent', 'count'], ascending=[True, False])

# Save the results to a CSV file
popular_industries_sorted.to_csv('/workspace/most_common_categories.csv', index=False)
