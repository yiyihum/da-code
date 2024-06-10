import pandas as pd
import matplotlib.pyplot as plt

# Load the orders data
orders_df = pd.read_csv('/workspace/orders.csv', parse_dates=['order_date'])

# Ensure the data is sorted by date
orders_df.sort_values(by='order_date', inplace=True)

# Group by store_id and order_date and count the orders for each day
daily_orders = orders_df.groupby(['store_id', 'order_date']).size().reset_index(name='order_count')

# Calculate the 30-day moving average of orders for each store
daily_orders['30_day_avg'] = daily_orders.groupby('store_id')['order_count'].transform(lambda x: x.rolling(window=30).mean())

# Pivot the data to have dates as the index and columns as store_ids with the moving average as values
pivot_df = daily_orders.pivot(index='order_date', columns='store_id', values='30_day_avg')

# Plotting
plt.figure(figsize=(10, 4))
for store_id in pivot_df.columns:
    plt.plot(pivot_df.index, pivot_df[store_id], label=f'Store {store_id}')

plt.title('30-Day Moving Average of Orders')
plt.xlabel('Date')
plt.ylabel('Average Orders')
plt.legend(title='store_id')
plt.tight_layout()
plt.savefig('/workspace/result.jpg')
