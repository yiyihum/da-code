import pandas as pd

# Load the data from CSV files
orders = pd.read_csv('orders.csv')
order_items = pd.read_csv('order_items.csv')
products = pd.read_csv('products.csv')
categories = pd.read_csv('categories.csv')

# Filter orders from 2016 to 2018
orders_filtered = orders[(orders['order_date'] >= '2016-01-01') & (orders['order_date'] <= '2018-12-31')]

# Merge the dataframes to get the required information
merged_df = orders_filtered.merge(order_items, on='order_id')                            .merge(products, on='product_id')                            .merge(categories, on='category_id')

# Use 'list_price_x' which is the list price from 'order_items'
merged_df['total_price'] = merged_df['list_price_x'] * (1 - merged_df['discount']) * merged_df['quantity']

# Now, group by category_name to sum up the quantities and total prices
result = merged_df.groupby('category_name').agg(
    total_quantity=('quantity', 'sum'),
    total_price=('total_price', 'sum')
).reset_index()

# Reorder the columns to match the sample_result.csv format
result = result[['total_quantity', 'total_price', 'category_name']]

# Save the result to 'result.csv'
result.to_csv('result.csv', index=False)
