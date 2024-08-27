import pandas as pd

# Define the path to the data directory
data_dir = 'data/'

# Read the date_dim and stations data for reference
date_dim_df = pd.read_csv('/workspace/date_dim.csv')
stations_df = pd.read_csv('/workspace/stations.csv')

# Create a mapping from full_date to date_key
date_mapping = pd.Series(date_dim_df.date_key.values, index=date_dim_df.full_date).to_dict()

# Create a mapping from station name to station id
station_mapping = pd.Series(stations_df.id.values, index=stations_df.station_name).to_dict()

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

# Initialize an empty DataFrame for rides
rides_df = pd.DataFrame()

# Process each file and extract ride information
for file in trip_data_files:
    # Read the current file
    df = pd.read_csv(f'{data_dir}{file}')
    
    # Convert start and stop times to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Stop Time'] = pd.to_datetime(df['Stop Time'])
    
    # Map the start and end station names to station ids
    df['Start Station ID'] = df['Start Station Name'].map(station_mapping)
    df['End Station ID'] = df['End Station Name'].map(station_mapping)
    
    # Map the start time to date_key
    df['date_key'] = df['Start Time'].dt.date.map(date_mapping)
    
    # Calculate trip duration in minutes and hours
    df['trip_minutes'] = df['Trip Duration'] // 60
    df['trip_hours'] = df['trip_minutes'] // 60
    
    # Determine if the trip duration is valid (between 60 seconds and 24 hours)
    df['valid_duration'] = (df['Trip Duration'] >= 60) & (df['Trip Duration'] <= 86400)
    
    # Select relevant columns to match the schema
    rides_info = df[['Trip Duration', 'Start Time', 'Stop Time', 'Start Station ID', 'End Station ID', 'Bike ID', 'date_key', 'trip_minutes', 'trip_hours', 'valid_duration']].copy()
    rides_info.columns = ['trip_duration', 'start_time', 'stop_time', 'start_station_id', 'end_station_id', 'bike_id', 'date_key', 'trip_minutes', 'trip_hours', 'valid_duration']
    
    # Append to the rides DataFrame
    rides_df = pd.concat([rides_df, rides_info], ignore_index=True)

# Add an id column as a primary key
rides_df.reset_index(inplace=True)
rides_df.rename(columns={'index': 'id'}, inplace=True)
rides_df['id'] += 1  # Start the primary key at 1

# Save the rides DataFrame to a CSV file
rides_df.to_csv('/workspace/rides.csv', index=False)
