import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
deliveries = pd.read_csv('deliveries.csv')
drivers = pd.read_csv('drivers.csv')
hubs = pd.read_csv('hubs.csv', encoding='ISO-8859-1')
stores = pd.read_csv('stores.csv', encoding='ISO-8859-1')
orders = pd.read_csv('orders.csv')

# Merge deliveries with orders to get store_id
deliveries_orders = pd.merge(deliveries, orders, left_on='delivery_order_id', right_on='order_id')

# Merge result with stores to get hub_id
deliveries_stores = pd.merge(deliveries_orders, stores, left_on='store_id', right_on='store_id')

# Merge result with hubs to get the hub city information
deliveries_hubs = pd.merge(deliveries_stores, hubs, left_on='hub_id', right_on='hub_id')

# Filter deliveries for CURITIBA
curitiba_deliveries = deliveries_hubs[deliveries_hubs['hub_city'] == 'CURITIBA']

# Merge with drivers to get driver modal information
curitiba_deliveries_drivers = pd.merge(curitiba_deliveries, drivers, left_on='driver_id', right_on='driver_id')

# Calculate the percentage of orders delivered by driver modal
driver_modal_percentage = curitiba_deliveries_drivers['driver_modal'].value_counts(normalize=True) * 100

# Plot the pie chart
plt.figure(figsize=(8, 8))
driver_modal_percentage.plot.pie(colors=["#ffdb00", "#ffb600"], autopct='%1.1f%%')
plt.title('Percentage of orders delivered by type of driver in CURITIBA')
plt.ylabel('')  # Hide the y-label

# Save the resulting image as result.jpg
plt.savefig('/workspace/result.jpg')
