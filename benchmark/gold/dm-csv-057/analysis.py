# Import pandas 
import pandas as pd 

# Load the customer_data
customer_data = pd.read_csv('user_demographics_v1.csv')

# Load the app_purchases
app_purchases = pd.read_csv('purchase_data.csv')

# Merge on the 'uid' field
purchase_data = app_purchases.merge(customer_data, on=['uid'], how='inner')
# Calculate the mean purchase price 
purchase_price_mean = purchase_data.price.agg('mean')

# Group the data 
grouped_purchase_data = purchase_data.groupby(by=['device', 'gender'])

# Aggregate the data
purchase_summary = grouped_purchase_data.agg({'price': ['mean', 'median', 'std']})

max_reg_date = "2018-02-17 00:00:00"
import numpy as np
from datetime import timedelta
# Find the month 1 values
month1 = np.where((purchase_data.reg_date < max_reg_date) &
                 (purchase_data.date < purchase_data.reg_date + timedelta(days=28)),
                  purchase_data.price, 
                  np.NaN)
                 
# Update the value in the DataFrame
purchase_data['month1'] = month1

print(purchase_data)
