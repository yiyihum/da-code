import pandas as pd
import numpy as np

# Function to draw bootstrap replicates
def draw_bs_reps(data, func, size=1):
    """Draw bootstrap replicates."""
    bs_replicates = np.empty(size)
    for i in range(size):
        bs_replicates[i] = func(np.random.choice(data, size=len(data)))
    return bs_replicates

# Load the data, skipping the initial comment lines
df = pd.read_csv('frog_tongue.csv', comment='#')

# Extract impact forces for Frog B and Frog D
frog_b_force = df[df['ID'] == 'B']['impact force (mN)'].values
frog_d_force = df[df['ID'] == 'D']['impact force (mN)'].values

# Compute mean impact force for Frog B and Frog D
mean_force_b = np.mean(frog_b_force)
mean_force_d = np.mean(frog_d_force)

# Compute combined mean
combined_mean = np.mean(np.concatenate((frog_b_force, frog_d_force)))

# Shift the datasets to have the same mean
frog_b_shifted = frog_b_force - mean_force_b + combined_mean
frog_d_shifted = frog_d_force - mean_force_d + combined_mean

# Compute 10,000 bootstrap replicates from shifted arrays
bs_replicates_b = draw_bs_reps(frog_b_shifted, np.mean, size=10000)
bs_replicates_d = draw_bs_reps(frog_d_shifted, np.mean, size=10000)

# Get the difference of the means
bs_diff_replicates = bs_replicates_b - bs_replicates_d

# Compute the observed difference in means
observed_diff = mean_force_b - mean_force_d

# Compute the p-value
p_value = np.sum(bs_diff_replicates >= observed_diff) / len(bs_diff_replicates)

# Save the result
result = pd.DataFrame({'p-value': [p_value]})
result.to_csv('result.csv', index=False)
