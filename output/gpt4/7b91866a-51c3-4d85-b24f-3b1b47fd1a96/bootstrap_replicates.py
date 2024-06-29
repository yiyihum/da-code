import pandas as pd
import numpy as np

# Function to generate bootstrap replicates
def bootstrap_replicate_1d(data, func):
    bs_sample = np.random.choice(data, len(data))
    return func(bs_sample)

# Set the seed
np.random.seed(42)

# Load the data, skipping the initial comment lines and using the correct separator
df = pd.read_csv('sheffield_weather_station.csv', comment='#', sep='\s+')

# Extract the annual rainfall
annual_rainfall = df['rain']

# Replace '---' with NaN and convert the column to float
annual_rainfall = pd.to_numeric(annual_rainfall, errors='coerce')

# Drop NaN values that represent missing data
annual_rainfall = annual_rainfall.dropna()

# Convert the cleaned annual rainfall data to a NumPy array
annual_rainfall = annual_rainfall.values

# Generate 10,000 bootstrap replicates of the variance
bs_replicates = np.empty(10000)
for i in range(10000):
    bs_replicates[i] = bootstrap_replicate_1d(annual_rainfall, np.var)

# Save the results
results = pd.DataFrame(bs_replicates, columns=['variance'])
results.to_csv('result.csv', index=False)
