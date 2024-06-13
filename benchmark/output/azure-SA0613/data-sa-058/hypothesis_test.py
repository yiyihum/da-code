import numpy as np
import pandas as pd

# Set the random seed
np.random.seed(42)

# Observed data
democrats_total = 244
democrats_yea = 153
fraction_yea_observed = democrats_yea / democrats_total

# Total votes
total_yea = 153 + 136
total_nay = 91 + 35
total_votes = total_yea + total_nay

# Function to generate permutation samples
def permutation_sample(data1, data2):
    data = np.concatenate((data1, data2))
    permuted_data = np.random.permutation(data)
    perm_sample_1 = permuted_data[:len(data1)]
    perm_sample_2 = permuted_data[len(data1):]
    return perm_sample_1, perm_sample_2

# Function to calculate permutation replicates
def draw_perm_reps(data_1, data_2, func, size=1):
    perm_replicates = np.empty(size)
    for i in range(size):
        perm_sample_1, perm_sample_2 = permutation_sample(data_1, data_2)
        perm_replicates[i] = func(perm_sample_1, perm_sample_2)
    return perm_replicates

# Test statistic: fraction of Democrat yea votes
def frac_yea_democrats(democrats, others):
    frac = np.sum(democrats) / len(democrats)
    return frac

# Create vote arrays
democrats = np.array([1] * democrats_yea + [0] * (democrats_total - democrats_yea))
others = np.array([1] * (total_yea - democrats_yea) + [0] * (total_votes - total_yea - (democrats_total - democrats_yea)))

# Generate permutation replicates
perm_replicates = draw_perm_reps(democrats, others, frac_yea_democrats, size=10000)

# Compute p-value
p_value = np.sum(perm_replicates <= fraction_yea_observed) / len(perm_replicates)

# Save the result
result = pd.DataFrame({'p_value': [p_value]})
result.to_csv('/workspace/result.csv', index=False)
