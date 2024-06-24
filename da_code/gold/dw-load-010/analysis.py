import pandas as pd
import sqlite3

# Read in CSV files
brands = pd.read_csv('dw-load-010\\brands.csv')
categories = pd.read_csv('dw-load-010\\categories.csv')
customers = pd.read_csv('dw-load-010\\customers.csv')
order_items = pd.read_csv('dw-load-010\\order_items.csv')
orders = pd.read_csv('dw-load-010\\orders.csv')
products = pd.read_csv('dw-load-010\\products.csv')
staffs = pd.read_csv('dw-load-010\\staffs.csv')
stocks = pd.read_csv('dw-load-010\\stocks.csv')
stores = pd.read_csv('dw-load-010\\stores.csv')

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

# Define and execute the query
query = """
SELECT
    c.first_name || ' ' || c.last_name AS customer_name,
    COUNT(s.order_id) AS total_transactions,
    RANK() OVER (ORDER BY COUNT(s.order_id) DESC) AS rank
FROM
    orders s
INNER JOIN
    customers c 
ON 
    s.customer_id = c.customer_id
GROUP BY
    c.customer_id
ORDER BY
    total_transactions DESC;
"""

# Execute the query and save the results to a new table in the database
result_df = pd.read_sql_query(query, connection)
result_df.to_sql('customer_transaction_summary', connection, if_exists='replace', index=False)

# Close the database connection
connection.close()