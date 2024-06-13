import pandas as pd
import numpy as np

# Set the random seed
np.random.seed(42)

# Load the dataset, skipping the initial rows with comments
df = pd.read_csv('frog_tongue.csv', comment='#')

# Filter the data for Frog D
frog_d = df[df['ID'] == 'D'].copy()

# Convert impact force from mN to N using .loc to avoid SettingWithCopyWarning
frog_d.loc[:, 'impact force (N)'] = frog_d['impact force (mN)'] / 1000

# Observed mean impact force for Frog D
observed_mean_d = frog_d['impact force (N)'].mean()

# Translate Frog D's impact forces to have the same mean as Frog E's impact forces
translated_force_d = frog_d['impact force (N)'] - observed_mean_d + 0.55

# Function to draw bootstrap replicates
def draw_bs_reps(data, func, size=1):
    """Draw bootstrap replicates."""
    bs_replicates = np.empty(size)
    for i in range(size):
        bs_replicates[i] = func(np.random.choice(data, size=len(data)))
    return bs_replicates

# Take 10,000 bootstrap replicates of the mean of the translated forces
bs_replicates = draw_bs_reps(translated_force_d, np.mean, size=10000)

# Compute the p-value
p_value = np.sum(bs_replicates <= observed_mean_d) / 10000

# Save the p-value to a CSV file
result = pd.DataFrame({'p-value': [p_value]})
result.to_csv('/workspace/result.csv', index=False)
