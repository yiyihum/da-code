import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sqlite3

# Read in CSV files
brands = pd.read_csv('Plot-line-4\\brands.csv')
categories = pd.read_csv('Plot-line-4\\categories.csv')
customers = pd.read_csv('Plot-line-4\\customers.csv')
order_items = pd.read_csv('Plot-line-4\\order_items.csv')
orders = pd.read_csv('Plot-line-4\\orders.csv')
products = pd.read_csv('Plot-line-4\\products.csv')
staffs = pd.read_csv('Plot-line-4\\staffs.csv')
stocks = pd.read_csv('Plot-line-4\\stocks.csv')
stores = pd.read_csv('Plot-line-4\\stores.csv')

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
WITH daily_orders AS (
    SELECT
        order_date,
        store_id,
        COUNT(*) AS orders
    FROM
        orders
    GROUP BY
        1,2
)

SELECT
    order_date,
    store_id,
    AVG(orders) OVER(PARTITION BY store_id 
                     ORDER BY order_date ASC
                     ROWS BETWEEN 14 PRECEDING AND 15 FOLLOWING) AS moving_avg_30d
FROM
    daily_orders;
"""

df = pd.read_sql_query(query, connection)

fig, ax = plt.subplots(figsize=(10,4))
sns.lineplot(data=df, x='order_date', y='moving_avg_30d', hue='store_id', ax=ax)
ax.set_xticks([])
ax.set_yticks([])
ax.set_ylabel('')
ax.set_xlabel('')
ax.set_title('30-Day Moving Average of Orders')
plt.savefig('result.jpg')
plt.show()