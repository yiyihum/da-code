import pandas as pd

# Load preprocessed weather data
weather_data = pd.read_csv('/workspace/preprocessed_weather_data.csv')
# Convert dt_iso back to datetime because it loses the datetime format after saving to CSV
weather_data['dt_iso'] = pd.to_datetime(weather_data['dt_iso'], utc=True)

# Load energy data
energy_data = pd.read_csv('/workspace/energy_dataset.csv')
energy_data['time'] = pd.to_datetime(energy_data['time'], utc=True)

# Filter weather data to only include timestamps present in energy data
weather_data_filtered = weather_data[weather_data['dt_iso'].isin(energy_data['time'])]

# Merge datasets on the time column
merged_data = pd.merge(energy_data, weather_data_filtered, left_on='time', right_on='dt_iso')

# Drop unnecessary columns
columns_to_drop = ['time', 'dt_iso', 'weather_id', 'weather_icon', 'weather_description', 'weather_main', 'city_name']
merged_data.drop(columns=columns_to_drop, inplace=True)

# Save the merged data to a new CSV file
merged_data.to_csv('/workspace/merged_data.csv', index=False)

# Print out the shape of the merged data as a checkpoint
print(f'Merged data shape: {merged_data.shape}')
