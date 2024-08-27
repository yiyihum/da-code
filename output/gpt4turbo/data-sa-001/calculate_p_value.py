import pandas as pd
from scipy.stats import ttest_ind

# Load the datasets
men_df = pd.read_csv('men_results.csv')
women_df = pd.read_csv('women_results.csv')

# Calculate the total number of goals for each match
men_goals = men_df['home_score'] + men_df['away_score']
women_goals = women_df['home_score'] + women_df['away_score']

# Perform two-sample t-test
t_stat, p_value = ttest_ind(men_goals, women_goals, equal_var=False)

# Determine whether to reject the null hypothesis
significance_level = 0.10
hypothesis_result = 'reject' if p_value < significance_level else 'fail to reject'

# Save the result to a CSV file
result_df = pd.DataFrame({
    't_statistic': [t_stat],
    'p_value': [p_value],
    'hypothesis_result': [hypothesis_result]
})
result_df.to_csv('result.csv', index=False)
