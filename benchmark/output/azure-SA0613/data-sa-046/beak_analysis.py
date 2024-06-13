import pandas as pd
import numpy as np

# Set the random seed for reproducibility
np.random.seed(42)

def bootstrap_replicate_1d(data, func):
    """Generate bootstrap replicate of 1D data."""
    bs_sample = np.random.choice(data, len(data))
    return func(bs_sample)

def draw_bs_reps(data, func, size=1):
    """Draw bootstrap replicates."""
    bs_replicates = np.array([bootstrap_replicate_1d(data, func) for _ in range(size)])
    return bs_replicates

# Load the datasets for 1975 and 2012
df_1975 = pd.read_csv('finch_beaks_1975.csv')
df_2012 = pd.read_csv('finch_beaks_2012.csv')

# Compute the length-to-depth ratios
ratio_1975 = df_1975['Beak length, mm'] / df_1975['Beak depth, mm']
ratio_2012 = df_2012['blength'] / df_2012['bdepth']

# Calculate the mean ratio for each year
mean_ratio_1975 = np.mean(ratio_1975)
mean_ratio_2012 = np.mean(ratio_2012)

# Generate 10,000 bootstrap replicates of the mean ratios
bs_replicates_1975 = draw_bs_reps(ratio_1975, np.mean, size=10000)
bs_replicates_2012 = draw_bs_reps(ratio_2012, np.mean, size=10000)

# Calculate the 99% confidence intervals for each year
conf_int_1975 = np.percentile(bs_replicates_1975, [0.5, 99.5])
conf_int_2012 = np.percentile(bs_replicates_2012, [0.5, 99.5])

# Write the results to 'result.csv'
results = pd.DataFrame({
    'year': [1975, 2012],
    'mean_ratio': [mean_ratio_1975, mean_ratio_2012],
    'conf_int_low': [conf_int_1975[0], conf_int_2012[0]],
    'conf_int_high': [conf_int_1975[1], conf_int_2012[1]]
})

results.to_csv('result.csv', index=False)
