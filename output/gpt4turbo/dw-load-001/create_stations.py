import pandas as pd

# Load the first citibike tripdata file to extract station information
tripdata_df = pd.read_csv('data/JC-201601-citibike-tripdata.csv')

# Extract unique stations from the start and end stations
start_stations = tripdata_df[['Start Station ID', 'Start Station Name', 'Start Station Latitude', 'Start Station Longitude']].rename(columns={
    'Start Station ID': 'id',
    'Start Station Name': 'station_name',
    'Start Station Latitude': 'latitude',
    'Start Station Longitude': 'longitude'
})
end_stations = tripdata_df[['End Station ID', 'End Station Name', 'End Station Latitude', 'End Station Longitude']].rename(columns={
    'End Station ID': 'id',
    'End Station Name': 'station_name',
    'End Station Latitude': 'latitude',
    'End Station Longitude': 'longitude'
})

# Combine start and end stations and drop duplicates
stations_df = pd.concat([start_stations, end_stations]).drop_duplicates().reset_index(drop=True)

# Save the stations table to a CSV file
stations_df.to_csv('/workspace/stations.csv', index=False)
