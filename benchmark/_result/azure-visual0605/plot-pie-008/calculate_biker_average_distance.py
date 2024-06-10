import pandas as pd

# Load the datasets
deliveries = pd.read_csv('deliveries.csv')
drivers = pd.read_csv('drivers.csv')
hubs = pd.read_csv('hubs.csv', encoding='ISO-8859-1')
orders = pd.read_csv('orders.csv')
# Specify encoding for the stores.csv file
stores = pd.read_csv('stores.csv', encoding='ISO-8859-1')

# Filter out deliveries that were not completed
deliveries = deliveries[deliveries['delivery_status'] == 'DELIVERED']

# Merge deliveries with drivers to get driver modal information
deliveries_drivers = pd.merge(deliveries, drivers, left_on='driver_id', right_on='driver_id')

# Filter out non-biker deliveries
biker_deliveries = deliveries_drivers[deliveries_drivers['driver_modal'] == 'BIKER']

# Merge biker deliveries with orders to get store_id
biker_deliveries_orders = pd.merge(biker_deliveries, orders, left_on='delivery_order_id', right_on='order_id')

# Merge result with stores to get hub_id
biker_deliveries_stores = pd.merge(biker_deliveries_orders, stores, left_on='store_id', right_on='store_id')

# Merge result with hubs to get the hub city information
biker_deliveries_hubs = pd.merge(biker_deliveries_stores, hubs, left_on='hub_id', right_on='hub_id')

# Calculate the average delivery distance for each hub city
average_distances = biker_deliveries_hubs.groupby('hub_city')['delivery_distance_meters'].mean().reset_index()

# Find the hub city with the largest average delivery distance
largest_average = average_distances.loc[average_distances['delivery_distance_meters'].idxmax()]

# Output the result to a CSV file
largest_average.to_csv('/workspace/largest_biker_average_distance.csv', index=False)
