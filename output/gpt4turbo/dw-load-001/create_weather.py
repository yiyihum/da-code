import pandas as pd

# Load the weather data file
weather_df = pd.read_csv('data/newark_airport_2016.csv')

# Select relevant columns and rename them according to the schema
weather_df = weather_df[['DATE', 'AWND', 'PRCP', 'SNOW', 'SNWD', 'TAVG', 'TMAX', 'TMIN']].rename(columns={
    'DATE': 'rec_date',
    'AWND': 'avg_wind',
    'PRCP': 'prcp',
    'SNOW': 'snow_amt',
    'SNWD': 'snow_depth',
    'TAVG': 'tavg',
    'TMAX': 'tmax',
    'TMIN': 'tmin'
})

# Convert 'rec_date' to datetime
weather_df['rec_date'] = pd.to_datetime(weather_df['rec_date'])

# Add boolean columns for rain and snow
weather_df['rain'] = weather_df['prcp'] > 0
weather_df['snow'] = weather_df['snow_amt'] > 0

# Add an id column
weather_df.insert(0, 'id', range(1, len(weather_df) + 1))

# Load the date_dim table to link the date_key
date_dim_df = pd.read_csv('/workspace/date_dim.csv')
date_dim_df['full_date'] = pd.to_datetime(date_dim_df['full_date'])

# Merge weather data with date_dim to get the date_key
weather_df = weather_df.merge(date_dim_df[['full_date', 'date_key']], left_on='rec_date', right_on='full_date', how='left')

# Select relevant columns for the final weather table
weather_df = weather_df[['id', 'rec_date', 'avg_wind', 'prcp', 'snow_amt', 'snow_depth', 'tavg', 'tmax', 'tmin', 'date_key', 'rain', 'snow']]

# Save the weather table to a CSV file
weather_df.to_csv('/workspace/weather.csv', index=False)
