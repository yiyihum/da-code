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

query = """
SELECT
    product_a,
    product_b,
    co_purchase_count
FROM 
    (
     SELECT
         p1.product_name AS product_a,
         p2.product_name AS product_b,
         COUNT(*) AS co_purchase_count
     FROM
         order_items s1
     INNER JOIN
         order_items s2 ON s1.order_id = s2.order_id AND s1.product_id <> s2.product_id
     INNER JOIN
         products p1 ON s1.product_id = p1.product_id
     INNER JOIN
         products p2 ON s2.product_id = p2.product_id
     GROUP BY
         p1.product_id, p2.product_id
    ) subquery
ORDER BY
    co_purchase_count DESC;
"""

df = pd.read_sql_query(query, connection)
max_co_purchase_row = df[df['co_purchase_count'] == df['co_purchase_count'].max()]
max_co_purchase_row.to_csv('Kaggle3-2\\result.csv', index=False)