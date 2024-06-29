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

# Initialize an empty DataFrame for trip_demo
trip_demo_df = pd.DataFrame()

# Process each file and extract user demographic information
for file in trip_data_files:
    # Read the current file
    df = pd.read_csv(f'{data_dir}{file}')
    
    # Extract user demographic information
    demo_df = df[['User Type', 'Birth Year', 'Gender']].copy()
    
    # Rename columns to match the schema
    demo_df.columns = ['user_type', 'birth_year', 'gender']
    
    # Map gender from numerical to string representation
    gender_map = {0: 'Unknown', 1: 'Male', 2: 'Female'}
    demo_df['gender'] = demo_df['gender'].map(gender_map)
    
    # Calculate age from birth year
    current_year = pd.Timestamp('now').year
    demo_df['age'] = current_year - demo_df['birth_year']
    
    # Append to the trip_demo DataFrame
    trip_demo_df = pd.concat([trip_demo_df, demo_df], ignore_index=True)

# Drop duplicates to ensure each combination of user_type, birth_year, and gender is only listed once
trip_demo_df.drop_duplicates(subset=['user_type', 'birth_year', 'gender'], inplace=True)

# Add an id column as a primary key
trip_demo_df.reset_index(inplace=True)
trip_demo_df.rename(columns={'index': 'id'}, inplace=True)
trip_demo_df['id'] += 1  # Start the primary key at 1

# Save the trip_demo DataFrame to a CSV file
trip_demo_df.to_csv('/workspace/trip_demo.csv', index=False)
