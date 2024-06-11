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

query = '''
        WITH total_spent AS
             (SELECT oi.order_id,
                     ot.customer_id,
                     c.first_name || ' ' || c.last_name AS name,  
                     ot.order_date, 
                     oi.product_id,
                     oi.quantity, 
                     oi.list_price, 
                     oi.discount, 
                     ((oi.quantity * oi.list_price) * (1-oi.discount)) AS total_sale_product
              FROM order_items as oi
              LEFT JOIN orders as ot
              ON oi.order_id = ot.order_id
              LEFT JOIN customers as c
              ON ot.customer_id = c.customer_id) 
              
        SELECT customer_id, name, ROUND(SUM(total_sale_product),2) AS total_spent 
        FROM total_spent
        GROUP BY customer_id, name  
        ORDER BY total_spent DESC
        '''


df = pd.read_sql_query(query, connection)
df.to_csv('result.csv', index=False)