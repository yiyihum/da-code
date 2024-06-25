import pandas as pd

# Load the data
data = pd.read_csv('/workspace/online.csv', parse_dates=['InvoiceDate'])

# Drop the unnamed column which seems to be an index
data.drop(columns=data.columns[0], inplace=True)

# Extract year and month from InvoiceDate
data['YearMonth'] = data['InvoiceDate'].dt.to_period('M')

# Determine the cohort for each customer (the month of the first purchase)
cohort_data = data.groupby('CustomerID')['YearMonth'].min().reset_index()
cohort_data.rename(columns={'YearMonth': 'Cohort'}, inplace=True)

# Merge the cohort data with the original data
merged_data = pd.merge(data, cohort_data, how='left', on='CustomerID')

# Group by CustomerID and Cohort and calculate the average unit price
average_price_data = merged_data.groupby(['Cohort', 'CustomerID'])['UnitPrice'].mean().reset_index()

# Save the results to the average_price.csv file
average_price_data.to_csv('/workspace/average_price.csv', index=False)
