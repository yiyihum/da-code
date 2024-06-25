import pandas as pd
from scipy.stats import ttest_ind

# Load the data
men_data = pd.read_csv('men_results.csv')
women_data = pd.read_csv('women_results.csv')

# Calculate the total number of goals for each match
men_goals = men_data['home_score'] + men_data['away_score']
women_goals = women_data['home_score'] + women_data['away_score']

# Perform a two-sample t-test
t_stat, p_value = ttest_ind(men_goals, women_goals, equal_var=False)

# Determine whether to reject the null hypothesis
significance_level = 0.10
reject_null = p_value < significance_level

# Save the result to a CSV file
result = pd.DataFrame({
    't_statistic': [t_stat],
    'p_value': [p_value],
    'reject_null_hypothesis': [reject_null]
})
result.to_csv('result.csv', index=False)
