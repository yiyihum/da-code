import pandas as pd
import matplotlib.pyplot as plt

# Read the data from CSV
df = pd.read_csv('/workspace/orders_data.csv')

# Convert the order_purchase_timestamp to datetime and extract the month and year
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['month_year'] = df['order_purchase_timestamp'].dt.to_period('M')

# Group by month_year and order_status, then count the orders
order_status_trends = df.groupby(['month_year', 'order_status']).size().unstack(fill_value=0)

# Plotting the data
plt.figure(figsize=(18, 6))
for status in order_status_trends.columns:
    plt.plot(order_status_trends.index.astype(str), order_status_trends[status], label=status)

# Formatting the plot
plt.title('Trend of Order Statuses Over Time')
plt.xlabel('Month')
plt.ylabel('Order Count')
plt.legend(title='Order Status')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot as 'result.png'
plt.savefig('/workspace/result.png')
