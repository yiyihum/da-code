import pandas as pd
from scipy.stats import mannwhitneyu

# Load the processed data
women_goals = pd.read_csv('/workspace/women_goals.csv')['total_goals'].tolist()
men_goals = pd.read_csv('/workspace/men_goals.csv')['total_goals'].tolist()

# Perform the Mann-Whitney U test
stat, p_value = mannwhitneyu(women_goals, men_goals, alternative='greater')

# Determine the conclusion based on the p-value
conclusion = 'reject' if p_value < 0.01 else 'fail to reject'

# Save the results to a CSV file
results = pd.DataFrame({
    'Statistic': [stat],
    'P-Value': [p_value],
    'Conclusion': [conclusion]
})
results.to_csv('/workspace/result.csv', index=False)

# Output the results to verify
print(results)
