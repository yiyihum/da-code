import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load datasets
energy_data = pd.read_csv('/workspace/energy_dataset.csv')
weather_data = pd.read_csv('/workspace/weather_features.csv')

# Convert time columns to datetime
energy_data['time'] = pd.to_datetime(energy_data['time'], utc=True)
weather_data['dt_iso'] = pd.to_datetime(weather_data['dt_iso'], utc=True)

# Encode categorical variables in weather data
label_encoder = LabelEncoder()
weather_data['city_name_encoded'] = label_encoder.fit_transform(weather_data['city_name'])

# Save the preprocessed weather data to a new CSV file
weather_data.to_csv('/workspace/preprocessed_weather_data.csv', index=False)

# Print out the shape of the datasets as a checkpoint
print(f'Energy data shape: {energy_data.shape}')
print(f'Weather data shape: {weather_data.shape}')
