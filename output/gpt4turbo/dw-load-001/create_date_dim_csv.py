import pandas as pd
from datetime import datetime

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

# Initialize an empty DataFrame for date_dim
date_dim_df = pd.DataFrame()

# Process each file and extract date information
for file in trip_data_files:
    # Read the current file
    df = pd.read_csv(f'{data_dir}{file}')
    
    # Extract start times and convert to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Create a DataFrame with date-related information
    dates_df = df['Start Time'].dt.date.unique()
    dates_df = pd.DataFrame(dates_df, columns=['full_date'])
    
    # Add additional date-related columns
    dates_df['full_date'] = pd.to_datetime(dates_df['full_date'])
    dates_df['month'] = dates_df['full_date'].dt.month
    dates_df['day'] = dates_df['full_date'].dt.day
    dates_df['month_name'] = dates_df['full_date'].dt.month_name()
    dates_df['day_name'] = dates_df['full_date'].dt.day_name()
    dates_df['financial_qtr'] = (dates_df['month'] - 1) // 3 + 1
    dates_df['weekend'] = dates_df['day_name'].isin(['Saturday', 'Sunday'])
    
    # Append to the date_dim DataFrame
    date_dim_df = pd.concat([date_dim_df, dates_df], ignore_index=True)

# Drop duplicates to ensure each date is only listed once
date_dim_df.drop_duplicates(subset='full_date', inplace=True)

# Add a date_key column as a primary key
date_dim_df.reset_index(inplace=True)
date_dim_df.rename(columns={'index': 'date_key'}, inplace=True)
date_dim_df['date_key'] += 1  # Start the primary key at 1

# Save the date_dim DataFrame to a CSV file
date_dim_df.to_csv('/workspace/date_dim.csv', index=False)
