import pandas as pd
import sqlite3

# Read in CSV files
brands = pd.read_csv('dw-load-009\\brands.csv')
categories = pd.read_csv('dw-load-009\\categories.csv')
customers = pd.read_csv('dw-load-009\\customers.csv')
order_items = pd.read_csv('dw-load-009\\order_items.csv')
orders = pd.read_csv('dw-load-009\\orders.csv')
products = pd.read_csv('dw-load-009\\products.csv')
staffs = pd.read_csv('dw-load-009\\staffs.csv')
stocks = pd.read_csv('dw-load-009\\stocks.csv')
stores = pd.read_csv('dw-load-009\\stores.csv')

# Create database connection to the 'order_customer' database
connection = sqlite3.connect('order_customer.db')

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

# Query to select distinct order and customer IDs
query = """
SELECT 
    DISTINCT
    order_id,
    customer_id
FROM 
    orders
WHERE
    order_id IN (
                  SELECT
                      DISTINCT
                      order_id
                  FROM
                      order_items
                  INNER JOIN
                      products
                  ON
                      order_items.product_id = products.product_id
                  AND
                      brand_id = 9
                  AND
                      discount >= .20
                 );
"""

# Execute the query and save results to a DataFrame
result_df = pd.read_sql_query(query, connection)

result_df.to_sql('order_customer', connection, if_exists='replace', index=False)

# Close the database connection
connection.close()

