import pandas as pd

# Load the datasets
companies = pd.read_csv('companies.csv')
dates = pd.read_csv('dates.csv')
funding = pd.read_csv('funding.csv')
industries = pd.read_csv('industries.csv')

# Convert date_joined to datetime and filter for the years 2019 to 2021
dates['date_joined'] = pd.to_datetime(dates['date_joined'])
filtered_dates = dates[(dates['date_joined'].dt.year >= 2019) & (dates['date_joined'].dt.year <= 2021)]

# Merge the datasets on company_id
merged_data = companies.merge(filtered_dates, on='company_id', how='inner')
merged_data = merged_data.merge(funding, on='company_id', how='inner')
merged_data = merged_data.merge(industries, on='company_id', how='inner')

# Save the merged and filtered data to a CSV file for further analysis
merged_data.to_csv('/workspace/filtered_merged_data.csv', index=False)
