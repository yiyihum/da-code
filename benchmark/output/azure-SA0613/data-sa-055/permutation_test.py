import pandas as pd
import numpy as np

# Set the seed for reproducibility
np.random.seed(42)

# Load the dataset
df = pd.read_csv('frog_tongue.csv', comment='#')

# Convert impact force from mN to N
df['impact force (N)'] = df['impact force (mN)'] / 1000

# Extract the impact forces for Frog B and Frog D
frog_b_force = df[df['ID'] == 'B']['impact force (N)'].values
frog_d_force = df[df['ID'] == 'D']['impact force (N)'].values

# Define a function to compute the difference of means
def diff_of_means(data_1, data_2):
    return np.mean(data_1) - np.mean(data_2)

# Compute the observed difference in mean impact force
observed_diff_means = diff_of_means(frog_b_force, frog_d_force)

# Initialize an array to store the permutation replicates
perm_replicates = np.empty(10000)

# Generate permutation replicates
for i in range(10000):
    # Permute the concatenated array: permuted_data
    permuted_data = np.random.permutation(np.concatenate((frog_b_force, frog_d_force)))
    
    # Split the permuted array into two: perm_sample_1, perm_sample_2
    perm_sample_1 = permuted_data[:len(frog_b_force)]
    perm_sample_2 = permuted_data[len(frog_b_force):]
    
    # Compute the test statistic
    perm_replicates[i] = diff_of_means(perm_sample_1, perm_sample_2)

# Compute the p-value
p_value = np.sum(perm_replicates >= observed_diff_means) / len(perm_replicates)

# Save the p-value to a CSV file
result = pd.DataFrame({'p-value': [p_value]})
result.to_csv('result.csv', index=False)

print('p-value:', p_value)
