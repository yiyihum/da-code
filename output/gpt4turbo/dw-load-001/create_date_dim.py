import pandas as pd

# Load the first citibike tripdata file to extract date information
tripdata_df = pd.read_csv('data/JC-201601-citibike-tripdata.csv')

# Extract the 'Start Time' column and convert it to datetime
tripdata_df['Start Time'] = pd.to_datetime(tripdata_df['Start Time'])

# Create a DataFrame for the date dimension table with unique dates
unique_dates = tripdata_df['Start Time'].dt.normalize().unique()
date_dim_df = pd.DataFrame(unique_dates, columns=['full_date'])

# Add additional columns based on the 'full_date' column
date_dim_df['date_key'] = range(1, len(date_dim_df) + 1)
date_dim_df['month'] = date_dim_df['full_date'].dt.month
date_dim_df['day'] = date_dim_df['full_date'].dt.day
date_dim_df['month_name'] = date_dim_df['full_date'].dt.month_name()
date_dim_df['day_name'] = date_dim_df['full_date'].dt.day_name()
date_dim_df['financial_qtr'] = ((date_dim_df['month'] - 1) // 3) + 1
date_dim_df['weekend'] = date_dim_df['day_name'].isin(['Saturday', 'Sunday']).astype(int)

# Save the date dimension table to a CSV file
date_dim_df.to_csv('/workspace/date_dim.csv', index=False)
