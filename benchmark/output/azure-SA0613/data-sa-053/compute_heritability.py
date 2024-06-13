import numpy as np
import pandas as pd

# Function to compute heritability
def heritability(parents, offspring):
    covariance_matrix = np.cov(parents, offspring)
    return covariance_matrix[0, 1] / covariance_matrix[0, 0]

# Function to perform pairs bootstrap
def draw_bs_pairs(x, y, size=1):
    inds = np.arange(len(x))
    bs_replicates = np.empty(size)
    
    for i in range(size):
        bs_inds = np.random.choice(inds, size=len(inds))
        bs_x, bs_y = x[bs_inds], y[bs_inds]
        bs_replicates[i] = heritability(bs_x, bs_y)
    
    return bs_replicates

# Set the random seed
np.random.seed(42)

# Load the data for G. fortis and G. scandens
fortis = pd.read_csv('fortis_beak_depth_heredity.csv')
scandens = pd.read_csv('scandens_beak_depth_heredity.csv')

# Compute the heritability for G. fortis
fortis_parents = (fortis['Male BD'] + fortis['Female BD']) / 2
fortis_offspring = fortis['Mid-offspr']
fortis_heritability = heritability(fortis_parents, fortis_offspring)

# Compute the heritability for G. scandens
scandens_parents = scandens['mid_parent']
scandens_offspring = scandens['mid_offspring']
scandens_heritability = heritability(scandens_parents, scandens_offspring)

# Acquire 1000 bootstrap replicates of heritability
fortis_replicates = draw_bs_pairs(fortis_parents, fortis_offspring, size=1000)
scandens_replicates = draw_bs_pairs(scandens_parents, scandens_offspring, size=1000)

# Compute the 95% confidence intervals
fortis_conf_int = np.percentile(fortis_replicates, [2.5, 97.5])
scandens_conf_int = np.percentile(scandens_replicates, [2.5, 97.5])

# Save the results
results = pd.DataFrame({
    'species': ['G. fortis', 'G. scandens'],
    'heritability': [fortis_heritability, scandens_heritability],
    'conf_int_low': [fortis_conf_int[0], scandens_conf_int[0]],
    'conf_int_high': [fortis_conf_int[1], scandens_conf_int[1]]
})
results.to_csv('result.csv', index=False)
