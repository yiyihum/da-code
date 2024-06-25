import pandas as pd
from datetime import datetime

# Load the data
orders = pd.read_csv('orders.csv')
order_items = pd.read_csv('order_items.csv')
products = pd.read_csv('products.csv')
categories = pd.read_csv('categories.csv')

# Merge the dataframes to get the required information
merged_df = orders.merge(order_items, on='order_id').merge(products, on='product_id')

# Convert order_date to datetime and extract year and month
merged_df['order_date'] = pd.to_datetime(merged_df['order_date'])
merged_df['year_month'] = merged_df['order_date'].dt.to_period('M')

# Group by category and year_month, then calculate the average units sold
monthly_avg = merged_df.groupby(['category_id', 'year_month'])['quantity'].sum().reset_index()
monthly_avg = monthly_avg.groupby('category_id')['quantity'].mean().reset_index()

# Map category_id to category_name
monthly_avg = monthly_avg.merge(categories, left_on='category_id', right_on='category_id')

# Rename columns to match the sample result and drop the category_id column
monthly_avg.rename(columns={'category_name': 'Category', 'quantity': 'Average Units Sold'}, inplace=True)
monthly_avg.drop('category_id', axis=1, inplace=True)

# Save the result to a CSV file
monthly_avg.to_csv('avg_units_sold.csv', index=False)
