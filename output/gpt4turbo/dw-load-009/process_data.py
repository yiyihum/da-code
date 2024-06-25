import pandas as pd
import sqlite3

# Load the necessary CSV files
brands_df = pd.read_csv('/workspace/brands.csv')
products_df = pd.read_csv('/workspace/products.csv')
order_items_df = pd.read_csv('/workspace/order_items.csv')
orders_df = pd.read_csv('/workspace/orders.csv')

# Identify all product_ids for the Trek brand
trek_brand_id = 9
trek_products = products_df[products_df['brand_id'] == trek_brand_id]

# Find all order_items with Trek product_ids and at least 20% discount
trek_order_items = order_items_df[
    (order_items_df['product_id'].isin(trek_products['product_id'])) &
    (order_items_df['discount'] >= 0.20)
]

# Join the order_items with orders to get the customer_id for each order
trek_orders = trek_order_items.merge(orders_df, on='order_id', how='inner')

# Select the unique combinations of order_id and customer_id
unique_combinations = trek_orders[['order_id', 'customer_id']].drop_duplicates()

# Save the result to a SQLite database
conn = sqlite3.connect('/workspace/order_customer.db')
unique_combinations.to_sql('order_customer', conn, if_exists='replace', index=False)
conn.close()
