import pandas as pd
from scipy.stats import mannwhitneyu

# Load the dataset
df = pd.read_csv('yulu_bike_sharing_dataset.csv')

# Group the data into holidays (grpA) and working days (grpB)
grpA = df[df['holiday'] == 1]['count']
grpB = df[df['workingday'] == 1]['count']

# Perform Mann-Whitney U test
u_stat, p_value = mannwhitneyu(grpA, grpB)

# Determine the hypothesis result
ab_hypothesis = "Strong Evidence To Reject NULL Hypothesis" if p_value < 0.05 else "No Evidence To Reject NULL Hypothesis"

# Comment on the result
comment = "A/B Groups Are Not Similar" if p_value < 0.05 else "A/B Groups Are Similar"

# Prepare the results for the CSV
results = {
    'test_type': ['Non Parametric'],
    'AB Hypothesis': [ab_hypothesis],
    'P-Value': [p_value],
    'Comment': [comment]
}

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to a CSV file
results_df.to_csv('ab_test_results.csv', index=False)
print(results_df)
