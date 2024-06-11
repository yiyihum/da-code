import pandas as pd

# Load the datasets with correct parsing of dates and times
energy_data = pd.read_csv('/workspace/energy_dataset.csv')
weather_data = pd.read_csv('/workspace/weather_features.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Convert the 'time' columns to datetime objects and localize to UTC
energy_data['time'] = pd.to_datetime(energy_data['time'], utc=True)
weather_data['dt_iso'] = pd.to_datetime(weather_data['dt_iso'], utc=True)
test_data['time'] = pd.to_datetime(test_data['time'], utc=True)

# Set the 'time' columns as the index
energy_data.set_index('time', inplace=True)
weather_data.set_index('dt_iso', inplace=True)
test_data.set_index('time', inplace=True)

# Merge the energy and weather datasets on the datetime index
merged_data = pd.merge(energy_data, weather_data, left_index=True, right_index=True, how='left')

# Fill missing values for numeric columns with the mean of the column
numeric_cols = merged_data.select_dtypes(include=['number']).columns
merged_data[numeric_cols] = merged_data[numeric_cols].fillna(merged_data[numeric_cols].mean())

# Drop non-numeric columns that are not needed for prediction
non_numeric_cols = ['city_name', 'weather_icon', 'weather_id', 'weather_description', 'weather_main']
merged_data.drop(columns=non_numeric_cols, inplace=True)

# Save the merged dataset to a CSV file
merged_data.to_csv('/workspace/merged_data.csv')

print('Merged data saved to /workspace/merged_data.csv')
