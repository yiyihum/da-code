import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

# Load the dataset
df = pd.read_csv('/workspace/drug_safety.csv')

# Count the number of adverse effects for each treatment group
adverse_effects_counts = df.groupby('trx')['adverse_effects'].value_counts().unstack(fill_value=0)

# Get the count of adverse effects and the total observations for each group
count_drug = adverse_effects_counts.loc['Drug', 'Yes']
nobs_drug = adverse_effects_counts.loc['Drug'].sum()
count_placebo = adverse_effects_counts.loc['Placebo', 'Yes']
nobs_placebo = adverse_effects_counts.loc['Placebo'].sum()

# Perform the Two-Sample Proportions Z-Test
z_score, p_value = proportions_ztest([count_drug, count_placebo], [nobs_drug, nobs_placebo])

# Save the results to the z_test_results.csv file
results_df = pd.DataFrame({'Z-score': [z_score], 'P-value': [p_value]})
results_df.to_csv('/workspace/z_test_results.csv', index=False)
