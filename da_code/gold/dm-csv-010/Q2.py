import pandas as pd

# Assume the data is in a CSV file named 'sales_data.csv'
# Read the CSV data into a DataFrame
data = pd.read_csv('Kaggle3-2_0//gold//result.csv')

# Group the data by 'category_name' and then calculate the variance of 'avg_units_sold'
variance_per_category = data.groupby('category_name')['avg_units_sold'].var()

# Print out the variance for each category
variance_per_category.to_csv('result.csv')