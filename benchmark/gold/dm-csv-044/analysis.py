import datetime as dt
import pandas as pd

online = pd.read_csv('DC3-1_0\\online.csv')

# Define a function that will parse the date
def get_day(date_str):
    date_dt = dt.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return dt.datetime(date_dt.year, date_dt.month, date_dt.day)

def get_date_int(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    day = df[column].dt.day
    return year, month, day

# Create InvoiceDay column
online['InvoiceDay'] = online['InvoiceDate'].apply(get_day)

# Group by CustomerID and select the InvoiceDay value
grouping = online.groupby('CustomerID')['InvoiceDay']

# Assign a minimum InvoiceDay value to the dataset
online['CohortDay'] = grouping.transform('min')

# Create a function to truncate given date to first day of the month
def get_month(x): 
    return dt.datetime(x.year, x.month, 1)

# Use the function to assign a CohortMonth
online['CohortMonth'] = online['CohortDay'].apply(get_month)

# Now, calculate the difference in years and months as before
invoice_year, invoice_month, _ = get_date_int(online, 'InvoiceDay')
cohort_year, cohort_month, _ = get_date_int(online, 'CohortMonth')

# Calculate difference in years
years_diff = invoice_year - cohort_year

# Calculate difference in months
months_diff = invoice_month - cohort_month

# Calculate the overall difference in months for the CohortIndex
online['CohortIndex'] = years_diff * 12 + months_diff + 1

# Finally group by CohortMonth and CohortIndex just as before
grouping = online.groupby(['CohortMonth', 'CohortIndex'])

# Calculate the average of the unit price 
cohort_data = grouping['UnitPrice'].mean()

# Reset the index of cohort_data
cohort_data = cohort_data.reset_index()

# Create a pivot 
average_price = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='UnitPrice')
print(average_price.round(1))