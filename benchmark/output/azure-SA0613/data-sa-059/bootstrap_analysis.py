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

# Set the seed
np.random.seed(42)

# Load the datasets
df_1975 = pd.read_csv('finch_beaks_1975.csv')
df_2012 = pd.read_csv('finch_beaks_2012.csv')

# Extract the beak depths for G. scandens species only
beak_depth_1975 = df_1975[df_1975['species'] == 'scandens']['Beak depth, mm'].values
beak_depth_2012 = df_2012[df_2012['species'] == 'scandens']['bdepth'].values

# Take 10,000 bootstrap replicates of the mean
bs_replicates_1975 = draw_bs_reps(beak_depth_1975, np.mean, size=10000)
bs_replicates_2012 = draw_bs_reps(beak_depth_2012, np.mean, size=10000)

# Compute the difference of the means
mean_diff = np.mean(beak_depth_2012) - np.mean(beak_depth_1975)

# Get the bootstrap replicates of the difference of the means
bs_diff_replicates = bs_replicates_2012 - bs_replicates_1975

# Compute the 95% confidence interval
conf_int = np.percentile(bs_diff_replicates, [2.5, 97.5])

# Save the results
results = {
    'mean_diff': mean_diff,
    '95%_conf_int_low': conf_int[0],
    '95%_conf_int_high': conf_int[1]
}
results_df = pd.DataFrame([results])
results_df.to_csv('result.csv', index=False)
