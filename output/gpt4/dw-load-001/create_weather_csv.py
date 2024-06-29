import pandas as pd

# Define the path to the Newark airport weather data CSV file
weather_data_file = 'data/newark_airport_2016.csv'

# Read the weather data file
weather_df = pd.read_csv(weather_data_file)

# Rename columns to match the schema and select relevant columns
weather_df.rename(columns={
    'DATE': 'rec_date',
    'AWND': 'avg_wind',
    'PRCP': 'prcp',
    'SNOW': 'snow_amt',
    'SNWD': 'snow_depth',
    'TAVG': 'tavg',
    'TMAX': 'tmax',
    'TMIN': 'tmin'
}, inplace=True)

# Select only the relevant columns
weather_df = weather_df[['rec_date', 'avg_wind', 'prcp', 'snow_amt', 'snow_depth', 'tavg', 'tmax', 'tmin']]

# Convert 'rec_date' to datetime
weather_df['rec_date'] = pd.to_datetime(weather_df['rec_date'])

# Add 'rain' and 'snow' boolean columns based on precipitation and snowfall amounts
weather_df['rain'] = weather_df['prcp'] > 0
weather_df['snow'] = weather_df['snow_amt'] > 0

# Add a placeholder 'date_key' column which will need to be updated to reference the 'date_dim' table
weather_df['date_key'] = None

# Add an 'id' column as a primary key
weather_df.reset_index(inplace=True)
weather_df.rename(columns={'index': 'id'}, inplace=True)
weather_df['id'] += 1  # Start the primary key at 1

# Save the weather DataFrame to a CSV file
weather_df.to_csv('/workspace/weather.csv', index=False)
