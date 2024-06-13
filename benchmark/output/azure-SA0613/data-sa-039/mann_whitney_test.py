import pandas as pd
from scipy.stats import mannwhitneyu

# Load the filtered results
men_results = pd.read_csv('/workspace/men_results_since_2002.csv')
women_results = pd.read_csv('/workspace/women_results_since_2002.csv')

# Extract the number of goals for each match
men_goals = men_results['home_score'] + men_results['away_score']
women_goals = women_results['home_score'] + women_results['away_score']

# Perform the Mann-Whitney U test
stat, p_value = mannwhitneyu(women_goals, men_goals, alternative='greater')

# Determine the conclusion based on the p-value
conclusion = 'reject' if p_value < 0.01 else 'fail to reject'

# Write the results to a CSV file
results_df = pd.DataFrame({
    'Statistic': [stat],
    'P-Value': [p_value],
    'Conclusion': [conclusion]
})
results_df.to_csv('/workspace/result.csv', index=False)
