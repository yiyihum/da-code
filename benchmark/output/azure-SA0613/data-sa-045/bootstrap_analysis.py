import pandas as pd
import numpy as np

# Set the seed for reproducibility
np.random.seed(42)

# Load the datasets for 1975 and 2012
df_1975 = pd.read_csv('finch_beaks_1975.csv')
df_2012 = pd.read_csv('finch_beaks_2012.csv')

# Standardize the column names
df_1975.rename(columns={'Beak depth, mm': 'beak_depth'}, inplace=True)
df_2012.rename(columns={'bdepth': 'beak_depth'}, inplace=True)

# Compute the mean of the combined dataset
combined_mean = np.mean(pd.concat([df_1975['beak_depth'], df_2012['beak_depth']]))

# Shift the samples
df_1975['shifted'] = df_1975['beak_depth'] - np.mean(df_1975['beak_depth']) + combined_mean
df_2012['shifted'] = df_2012['beak_depth'] - np.mean(df_2012['beak_depth']) + combined_mean

# Function to draw bootstrap replicates
def draw_bs_reps(data, func, size=1):
    return np.array([func(np.random.choice(data, size=len(data))) for _ in range(size)])

# Get Bootstrap replicates of shifted data sets
bs_replicates_1975 = draw_bs_reps(df_1975['shifted'], np.mean, size=10000)
bs_replicates_2012 = draw_bs_reps(df_2012['shifted'], np.mean, size=10000)

# Compute replicates of the difference of means
bs_diff_replicates = bs_replicates_2012 - bs_replicates_1975

# Compute the p-value
actual_diff = np.mean(df_2012['beak_depth']) - np.mean(df_1975['beak_depth'])
p_value = np.sum(bs_diff_replicates >= actual_diff) / len(bs_diff_replicates)

# Write the p-value to 'result.csv' in the specified format
result_df = pd.DataFrame({'p-val': [p_value]})
result_df.to_csv('result.csv', index=False)
