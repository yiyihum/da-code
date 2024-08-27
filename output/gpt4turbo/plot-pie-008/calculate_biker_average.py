import pandas as pd

# Load the data
deliveries = pd.read_csv('deliveries.csv')
drivers = pd.read_csv('drivers.csv')
orders = pd.read_csv('orders.csv')

# Attempt to read stores.csv with ISO-8859-1 encoding
try:
    stores = pd.read_csv('stores.csv', encoding='utf-8')
except UnicodeDecodeError:
    stores = pd.read_csv('stores.csv', encoding='ISO-8859-1')

# Attempt to read hubs.csv with ISO-8859-1 encoding
try:
    hubs = pd.read_csv('hubs.csv', encoding='utf-8')
except UnicodeDecodeError:
    hubs = pd.read_csv('hubs.csv', encoding='ISO-8859-1')

# Merge deliveries with drivers to get the driver mode
deliveries_with_mode = pd.merge(deliveries, drivers, how='left', on='driver_id')

# Merge orders with stores to get the hub_id for each order
orders_with_hub = pd.merge(orders, stores, how='left', on='store_id')

# Merge the result with deliveries to associate each delivery with a hub
deliveries_with_hub = pd.merge(deliveries_with_mode, orders_with_hub, how='left', left_on='delivery_order_id', right_on='order_id')

# Filter out the deliveries made by bikers
biker_deliveries = deliveries_with_hub[deliveries_with_hub['driver_modal'] == 'BIKER']

# Merge biker deliveries with hubs to get the hub city
biker_deliveries_with_city = pd.merge(biker_deliveries, hubs, how='left', on='hub_id')

# Calculate the average delivery distance for bikers in each hub city
biker_avg_distance_by_city = biker_deliveries_with_city.groupby('hub_city')['delivery_distance_meters'].mean().reset_index()

# Find the city with the largest biker average delivery distance
largest_avg_distance_city = biker_avg_distance_by_city.loc[biker_avg_distance_by_city['delivery_distance_meters'].idxmax()]

# Output the city name and its average delivery distance
print(largest_avg_distance_city)
