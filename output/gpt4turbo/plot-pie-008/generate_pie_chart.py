import matplotlib.pyplot as plt
import pandas as pd

# Load the data
deliveries = pd.read_csv('deliveries.csv')
drivers = pd.read_csv('drivers.csv')
orders = pd.read_csv('orders.csv')
stores = pd.read_csv('stores.csv', encoding='ISO-8859-1')
hubs = pd.read_csv('hubs.csv', encoding='ISO-8859-1')

# Merge deliveries with drivers to get the driver mode
deliveries_with_mode = pd.merge(deliveries, drivers, how='left', on='driver_id')

# Merge orders with stores to get the hub_id for each order
orders_with_hub = pd.merge(orders, stores, how='left', on='store_id')

# Merge the result with deliveries to associate each delivery with a hub
deliveries_with_hub = pd.merge(deliveries_with_mode, orders_with_hub, how='left', left_on='delivery_order_id', right_on='order_id')

# Merge biker deliveries with hubs to get the hub city
deliveries_with_city = pd.merge(deliveries_with_hub, hubs, how='left', on='hub_id')

# Filter deliveries for CURITIBA and by driver mode
curitiba_deliveries = deliveries_with_city[deliveries_with_city['hub_city'] == 'CURITIBA']
driver_mode_counts = curitiba_deliveries['driver_modal'].value_counts()

# Define the colors and figure size as per plot.yaml
colors = ["#ffdb00", "#ffb600"]
figsize = [8.0, 8.0]

# Create the pie chart
plt.figure(figsize=figsize)
plt.pie(driver_mode_counts, labels=driver_mode_counts.index, colors=colors, autopct='%1.1f%%', startangle=140)
plt.title("Percentage of orders delivered by type of driver in CURITIBA")

# Save the pie chart as result.jpg
plt.savefig('result.jpg')
