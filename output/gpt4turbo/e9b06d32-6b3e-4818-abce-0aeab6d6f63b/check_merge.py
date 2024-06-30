import pandas as pd

# Load the data from CSV files
orders = pd.read_csv('orders.csv')
order_items = pd.read_csv('order_items.csv')
products = pd.read_csv('products.csv')
categories = pd.read_csv('categories.csv')

# Check the merge process by merging one DataFrame at a time and checking the columns
merged_orders_order_items = orders.merge(order_items, on='order_id')
print("Columns after merging orders and order_items:", merged_orders_order_items.columns)

merged_with_products = merged_orders_order_items.merge(products, on='product_id')
print("Columns after merging with products:", merged_with_products.columns)

merged_with_categories = merged_with_products.merge(categories, on='category_id')
print("Columns after merging with categories:", merged_with_categories.columns)
