import pandas as pd

# Define the path to the data directory
data_dir = 'data/'

# List of all Citi Bike trip data CSV files
trip_data_files = [
    'JC-201601-citibike-tripdata.csv',
    'JC-201602-citibike-tripdata.csv',
    'JC-201603-citibike-tripdata.csv',
    'JC-201604-citibike-tripdata.csv',
    'JC-201605-citibike-tripdata.csv',
    'JC-201606-citibike-tripdata.csv',
    'JC-201607-citibike-tripdata.csv',
    'JC-201608-citibike-tripdata.csv',
    'JC-201609-citibike-tripdata.csv',
    'JC-201610-citibike-tripdata.csv',
    'JC-201611-citibike-tripdata.csv',
    'JC-201612-citibike-tripdata.csv'
]

# Initialize an empty list to collect DataFrames
stations_list = []

# Process each file and append to the stations list
for file in trip_data_files:
    # Read the current file
    df = pd.read_csv(f'{data_dir}{file}')
    
    # Extract station information
    start_stations = df[['Start Station ID', 'Start Station Name', 'Start Station Latitude', 'Start Station Longitude']]
    end_stations = df[['End Station ID', 'End Station Name', 'End Station Latitude', 'End Station Longitude']]
    
    # Rename columns to match the schema
    start_stations.columns = ['id', 'station_name', 'latitude', 'longitude']
    end_stations.columns = ['id', 'station_name', 'latitude', 'longitude']
    
    # Append to the stations list
    stations_list.append(start_stations)
    stations_list.append(end_stations)

# Concatenate all DataFrames in the list
stations_df = pd.concat(stations_list, ignore_index=True)

# Drop duplicates to ensure each station is only listed once
stations_df.drop_duplicates(subset='id', inplace=True)

# Save the stations DataFrame to a CSV file
stations_df.to_csv('/workspace/stations.csv', index=False)
