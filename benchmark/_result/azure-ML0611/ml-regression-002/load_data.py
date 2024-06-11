import pandas as pd

# Load the datasets
energy_data = pd.read_csv('/workspace/energy_dataset.csv')
weather_data = pd.read_csv('/workspace/weather_features.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Display the first few rows of each dataframe to confirm successful loading
print(energy_data.head())
print(weather_data.head())
print(test_data.head())
