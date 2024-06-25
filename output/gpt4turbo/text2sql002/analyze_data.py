import pandas as pd

# Load the data from CSV files
companies_df = pd.read_csv('/workspace/companies.csv')
dates_df = pd.read_csv('/workspace/dates.csv')
industries_df = pd.read_csv('/workspace/industries.csv')

# Merge the dataframes on 'company_id'
merged_df = companies_df.merge(dates_df, on='company_id').merge(industries_df, on='company_id')

# Find the oldest businesses on each continent by getting the minimum 'year_founded' for each continent
oldest_years_per_continent = merged_df.groupby('continent')['year_founded'].min().reset_index()

# Filter the merged dataframe to only include the oldest businesses per continent
oldest_companies_df = merged_df[merged_df.apply(lambda x: x['year_founded'] == oldest_years_per_continent[oldest_years_per_continent['continent'] == x['continent']]['year_founded'].values[0], axis=1)]

# Group by 'continent' and 'industry' to get the count of each category
category_counts_df = oldest_companies_df.groupby(['continent', 'industry']).size().reset_index(name='count')

# Save the result to a CSV file without applying the count > 5 filter
category_counts_df.to_csv('/workspace/category_counts.csv', index=False)
