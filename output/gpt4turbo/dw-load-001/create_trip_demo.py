import pandas as pd

# Load the first citibike tripdata file to extract user demographic information
tripdata_df = pd.read_csv('data/JC-201601-citibike-tripdata.csv')

# Extract user demographic information
trip_demo_df = tripdata_df[['User Type', 'Birth Year', 'Gender']].drop_duplicates().reset_index(drop=True)
trip_demo_df = trip_demo_df.rename(columns={
    'User Type': 'user_type',
    'Birth Year': 'birth_year',
    'Gender': 'gender'
})

# Convert gender from numerical to string representation
gender_mapping = {0: 'Unknown', 1: 'Male', 2: 'Female'}
trip_demo_df['gender'] = trip_demo_df['gender'].map(gender_mapping)

# Calculate age from birth year
current_year = pd.to_datetime('now').year
trip_demo_df['age'] = current_year - trip_demo_df['birth_year']

# Add an id column
trip_demo_df.insert(0, 'id', range(1, len(trip_demo_df) + 1))

# Save the trip_demo table to a CSV file
trip_demo_df.to_csv('/workspace/trip_demo.csv', index=False)
