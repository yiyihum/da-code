import pandas as pd

# Load the dataset with low_memory=False to handle mixed types
df = pd.read_csv('/workspace/city_temperature.csv', low_memory=False)

# Filter out records with an average temperature less than -70 Fahrenheit
df_filtered = df[df['AvgTemperature'] > -70].copy()

# Convert Fahrenheit to Celsius using .loc to avoid SettingWithCopyWarning
df_filtered.loc[:, 'AvgTemperatureC'] = (df_filtered['AvgTemperature'] - 32) * 5/9

# Save the filtered and converted dataset to a new CSV file for further processing
df_filtered.to_csv('/workspace/filtered_temperature.csv', index=False)
