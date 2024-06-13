import pandas as pd
import numpy as np

# Function to draw bootstrap replicates
def draw_bs_reps(data, func, size=1):
    """Draw bootstrap replicates."""
    bs_replicates = np.empty(size)
    for i in range(size):
        bs_sample = np.random.choice(data, len(data))
        bs_replicates[i] = func(bs_sample)
    return bs_replicates

# Set the random seed
np.random.seed(42)

# Read the CSV file, skipping initial lines with comments and specifying the delimiter
data = pd.read_csv('sheffield_weather_station.csv', comment='#', delim_whitespace=True)

# Replace '---' with NaN and drop rows with missing values in 'rain' column
data['rain'].replace('---', np.nan, inplace=True)
data.dropna(subset=['rain'], inplace=True)
data['rain'] = data['rain'].astype(float)

# Group by year and sum the rainfall to get annual rainfall
annual_rainfall = data.groupby('yyyy')['rain'].sum()

# Calculate 10,000 bootstrap replicates of the variance
bs_replicates = draw_bs_reps(annual_rainfall, np.var, size=10000)

# Convert the variance from square millimeters to square centimeters
bs_replicates /= 100

# Compute the PDF
bin_edges = np.linspace(np.min(bs_replicates), np.max(bs_replicates), 51)
pdf, _ = np.histogram(bs_replicates, bins=bin_edges, density=True)
bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])

# Save the results to a CSV file
results = pd.DataFrame({'bin_center': bin_centers, 'pdf': pdf})
results.to_csv('result.csv', index=False)
