import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')
test_data['time'] = pd.to_datetime(test_data['time'], utc=True)

# Load the preprocessed weather data
weather_data = pd.read_csv('/workspace/preprocessed_weather_data.csv')
weather_data['dt_iso'] = pd.to_datetime(weather_data['dt_iso'], utc=True)

# Merge test data with weather data
test_data_merged = pd.merge(test_data, weather_data, left_on='time', right_on='dt_iso')

# Drop unnecessary columns from the merged test data
columns_to_drop = ['time', 'dt_iso', 'weather_id', 'weather_icon', 'weather_description', 'weather_main', 'city_name']
test_data_merged.drop(columns=columns_to_drop, inplace=True)

# Save the preprocessed test data to a new CSV file
test_data_merged.to_csv('/workspace/preprocessed_test_data.csv', index=False)

print("Test data preprocessed and saved.")
