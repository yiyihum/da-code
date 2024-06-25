import pandas as pd

# Load the deliveries data
deliveries = pd.read_csv('deliveries.csv')

# Filter out the deliveries made by bikers
biker_deliveries = deliveries[deliveries['driver_mode'] == 'biker']

# Calculate the average delivery distance for bikers in each hub city
biker_avg_distance_by_city = biker_deliveries.groupby('hub')['delivery_distance'].mean().reset_index()

# Find the city with the largest biker average delivery distance
largest_avg_distance_city = biker_avg_distance_by_city.loc[biker_avg_distance_by_city['delivery_distance'].idxmax()]

# Output the city name and its average delivery distance
print(largest_avg_distance_city)
