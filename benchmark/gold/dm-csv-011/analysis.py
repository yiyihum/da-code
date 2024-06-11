import pandas as pd
import sqlite3

# Read in CSV files
brands = pd.read_csv('Kaggle3-2\\brands.csv')
categories = pd.read_csv('Kaggle3-2\\categories.csv')
customers = pd.read_csv('Kaggle3-2\\customers.csv')
order_items = pd.read_csv('Kaggle3-2\\order_items.csv')
orders = pd.read_csv('Kaggle3-2\\orders.csv')
products = pd.read_csv('Kaggle3-2\\products.csv')
staffs = pd.read_csv('Kaggle3-2\\staffs.csv')
stocks = pd.read_csv('Kaggle3-2\\stocks.csv')
stores = pd.read_csv('Kaggle3-2\\stores.csv')

# Create database connection
connection = sqlite3.connect('bike_store.db')

# Insert data into database
brands.to_sql('brands', connection, if_exists='replace', index=False)
categories.to_sql('categories', connection, if_exists='replace', index=False)
customers.to_sql('customers', connection, if_exists='replace', index=False)
order_items.to_sql('order_items', connection, if_exists='replace', index=False)
orders.to_sql('orders', connection, if_exists='replace', index=False)
products.to_sql('products', connection, if_exists='replace', index=False)
staffs.to_sql('staffs', connection, if_exists='replace', index=False)
stocks.to_sql('stocks', connection, if_exists='replace', index=False)
stores.to_sql('stores', connection, if_exists='replace', index=False)

#Create a temp table to join products, brands and categories
#Join temp table to order_items and save as new table
query = """
WITH temp_products as (
    SELECT 
        products.product_id,
        products.product_name,
        products.model_year,
        brands.brand_name,
        categories.category_name
    FROM products
    JOIN brands ON products.brand_id = brands.brand_id
    JOIN categories ON products.category_id = categories.category_id
)

SELECT
    order_items.quantity,
    order_items.list_price,
    order_items.discount,
    temp_products.product_name,
    temp_products.model_year,
    temp_products.brand_name,
    temp_products.category_name
FROM order_items
JOIN temp_products ON order_items.product_id = temp_products.product_id

"""
orders2 = pd.read_sql_query(query, connection)
orders2.to_sql('orders2', connection, if_exists='replace', index=False)
# print(orders2)

#Determine the most sold and highest grossing product by category
query = """

SELECT
    SUM(quantity) as total_quantity,
    ROUND(SUM(list_price*(1-discount)),2) as total_price,
    category_name
FROM orders2
GROUP BY
    category_name
ORDER BY
    total_price desc
"""
categories_df = pd.read_sql_query(query, connection)
categories_df.to_csv('result.csv', index=False)
