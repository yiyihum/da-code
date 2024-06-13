import pandas as pd
from scipy.stats import mannwhitneyu

# Load the dataset
data = pd.read_csv('drug_safety.csv')

# Separate the ages for Drug and Placebo groups
drug_ages = data[data['trx'] == 'Drug']['age']
placebo_ages = data[data['trx'] == 'Placebo']['age']

# Perform the Mann-Whitney U test
stat, p_value = mannwhitneyu(drug_ages, placebo_ages, alternative='two-sided')

# Save the p-value to the CSV file
result_df = pd.DataFrame({'p-val': [p_value]})
result_df.to_csv('age_group_effects_p_value.csv', index=False)
