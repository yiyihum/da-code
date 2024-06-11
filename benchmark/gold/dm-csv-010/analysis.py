import pandas as pd
import sqlite3

# Read in CSV files
brands = pd.read_csv('Kaggle3-2_0\\brands.csv')
categories = pd.read_csv('Kaggle3-2_0\\categories.csv')
customers = pd.read_csv('Kaggle3-2_0\\customers.csv')
order_items = pd.read_csv('Kaggle3-2_0\\order_items.csv')
orders = pd.read_csv('Kaggle3-2_0\\orders.csv')
products = pd.read_csv('Kaggle3-2_0\\products.csv')
staffs = pd.read_csv('Kaggle3-2_0\\staffs.csv')
stocks = pd.read_csv('Kaggle3-2_0\\stocks.csv')
stores = pd.read_csv('Kaggle3-2_0\\stores.csv')

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
WITH product_categories AS (
    SELECT
        product_id,
        category_name
    FROM
        products
    INNER JOIN
        categories
    ON
        products.category_id = categories.category_id
),

product_sales_ym AS (
    SELECT
        strftime('%Y', order_date) AS year,
        strftime('%m', order_date) AS month,
        product_id,
        SUM(quantity) AS units_sold
    FROM
        orders
    INNER JOIN
        order_items
    ON
        orders.order_id = order_items.order_id
    GROUP BY
        1,2,3
)

SELECT
    month,
    category_name,
    AVG(units_sold) AS avg_units_sold
FROM
    product_sales_ym
INNER JOIN
    product_categories
ON
    product_sales_ym.product_id = product_categories.product_id
GROUP BY
    1,2;
"""

df = pd.read_sql_query(query, connection)
# Save the DataFrame to a JSON file
# json_file_path = 'Kaggle3-2_0//gold//result.json'  # Define the path to save the JSON file
# df.to_json(json_file_path, orient='records', lines=True)
df.to_csv('Kaggle3-2_0//gold//result.csv')
# Close the connection
connection.close()