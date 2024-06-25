import pandas as pd
from datetime import datetime

# Load the data
companies = pd.read_csv('/workspace/companies.csv')
dates = pd.read_csv('/workspace/dates.csv')
funding = pd.read_csv('/workspace/funding.csv')
industries = pd.read_csv('/workspace/industries.csv')

# Convert date_joined to datetime and filter for the last three years
dates['date_joined'] = pd.to_datetime(dates['date_joined'])
three_years_ago = datetime.now() - pd.DateOffset(years=3)
recent_companies = dates[dates['date_joined'] > three_years_ago]

# Merge the datasets on company_id
merged_data = recent_companies.merge(companies, on='company_id', how='inner')
merged_data = merged_data.merge(funding, on='company_id', how='inner')
merged_data = merged_data.merge(industries, on='company_id', how='inner')

# Calculate the average valuation by sector
sector_valuation = merged_data.groupby('industry')['valuation'].mean().reset_index()

# Sort sectors by average valuation
sector_valuation_sorted = sector_valuation.sort_values(by='valuation', ascending=False)

# Save the result to a CSV file
sector_valuation_sorted.to_csv('/workspace/sector_valuation.csv', index=False)

# Identify standout new companies in the leading sectors
# For this, we consider standout companies to be those with valuations above the 75th percentile in their sector
standout_companies = merged_data.copy()
try:
    standout_companies['valuation_percentile'] = standout_companies.groupby('industry')['valuation'].transform(
        lambda x: pd.qcut(x, q=4, labels=False, duplicates='drop') + 1
    )
except ValueError as e:
    print(f"An error occurred while calculating valuation percentiles: {e}")

# Filter for standout companies (in the top quartile)
standout_companies = standout_companies[standout_companies['valuation_percentile'] == 4]

# Save the standout companies to a CSV file
standout_companies.to_csv('/workspace/standout_companies.csv', index=False)
