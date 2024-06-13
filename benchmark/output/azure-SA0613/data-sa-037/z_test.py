import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

# Load the dataset
data = pd.read_csv('/workspace/testdata.csv')

# Separate the control and treatment groups
control_data = data[data['Group'] == 'control']
treatment_data = data[data['Group'] == 'treatment']

# Calculate the number of successes (conversions) and the number of observations for each group
control_successes = control_data['Converted'].sum()
treatment_successes = treatment_data['Converted'].sum()
control_observations = control_data.shape[0]
treatment_observations = treatment_data.shape[0]

# Perform z-test
z_stat, p_value = proportions_ztest(
    [treatment_successes, control_successes],
    [treatment_observations, control_observations],
    alternative='larger'  # because we are testing if the treatment conversion rate is greater
)

# Output the p-value
print(f"Z-statistic: {z_stat}, p-value: {p_value}")
