import pandas as pd
from datetime import datetime

# Load the datasets
companies = pd.read_csv('companies.csv')
dates = pd.read_csv('dates.csv')
funding = pd.read_csv('funding.csv')
industries = pd.read_csv('industries.csv')

# Merge the datasets on company_id
merged_data = companies.merge(dates, on='company_id').merge(funding, on='company_id').merge(industries, on='company_id')

# Convert date_joined to datetime and filter for the last three years
merged_data['date_joined'] = pd.to_datetime(merged_data['date_joined'])
three_years_ago = datetime.now() - pd.DateOffset(years=3)
filtered_data = merged_data[merged_data['date_joined'] > three_years_ago]

# Calculate the average valuation for each sector
sector_valuation = filtered_data.groupby('industry')['valuation'].mean().reset_index()

# Identify standout new companies in those leading sectors
# We define standout companies as those with valuations above the 75th percentile within their sector
def standout_companies(group):
    threshold = group['valuation'].quantile(0.75)
    standout = group.loc[group['valuation'] > threshold].copy()
    # Assign 'industry' for the entire DataFrame
    standout['industry'] = group.name  # Correctly assign the scalar value
    return standout

# Apply the function to each sector group and include the 'industry' column
standout_companies = filtered_data.groupby('industry', group_keys=False).apply(standout_companies, include_groups=False)

# Combine the average sector valuation with standout companies
result = sector_valuation.merge(standout_companies, on='industry', suffixes=('_avg', '_standout'))

# Save the result to a CSV file
result.to_csv('result.csv', index=False)
