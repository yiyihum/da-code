import pandas as pd
import numpy as np

# Load the data
data = pd.read_csv('online.csv', parse_dates=['InvoiceDate'])

# Create a cohort group based on the first purchase date of each customer
data['CohortGroup'] = data.groupby('CustomerID')['InvoiceDate'].transform('min').dt.to_period('M')

# Create a period column based on the InvoiceDate
data['OrderPeriod'] = data.InvoiceDate.dt.to_period('M')

# Determine the number of unique customers in each group
cohorts = data.groupby(['CohortGroup', 'OrderPeriod']).agg({'CustomerID': pd.Series.nunique})

# Make the column names more meaningful
cohorts.rename(columns={'CustomerID': 'TotalCustomers'}, inplace=True)

# Create a DataFrame with the number of total unique customers in each cohort
cohorts.reset_index(inplace=True)
cohorts.set_index(['CohortGroup', 'OrderPeriod'], inplace=True)

# Create a cohort period to understand how many periods are between the first purchase and subsequent purchases
def cohort_period(df):
    df['CohortPeriod'] = np.arange(len(df)) + 1
    return df

cohorts = cohorts.groupby(level=0).apply(cohort_period)

# Pivot the data to have CohortPeriod as columns and each row will be a CohortGroup
retention = cohorts.pivot_table(index='CohortGroup', columns='CohortPeriod', values='TotalCustomers')

# Divide by the cohort size (i.e., the number of customers in the first period) to get the retention rate
cohort_group_size = retention.iloc[:,0]
retention = retention.divide(cohort_group_size, axis=0)

# Reset the index before saving
retention.reset_index(inplace=True)

# Save the retention data to a CSV file
retention.to_csv('retension.csv', index=False)
