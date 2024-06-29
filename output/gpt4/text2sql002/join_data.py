import pandas as pd

# Load the datasets
companies_df = pd.read_csv('/workspace/companies.csv')
dates_df = pd.read_csv('/workspace/dates.csv')

# Merge the datasets on 'company_id'
merged_df = pd.merge(companies_df, dates_df, on='company_id')

# Save the merged data to a new CSV file for further processing
merged_df.to_csv('/workspace/merged_companies_dates.csv', index=False)
