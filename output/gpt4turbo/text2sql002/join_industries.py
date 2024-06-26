import pandas as pd

# Load the merged companies and dates dataset
merged_companies_dates_df = pd.read_csv('/workspace/merged_companies_dates.csv')

# Load the industries dataset
industries_df = pd.read_csv('/workspace/industries.csv')

# Merge the datasets on 'company_id'
merged_all_df = pd.merge(merged_companies_dates_df, industries_df, on='company_id')

# Save the fully merged data to a new CSV file for further processing
merged_all_df.to_csv('/workspace/merged_all_data.csv', index=False)
