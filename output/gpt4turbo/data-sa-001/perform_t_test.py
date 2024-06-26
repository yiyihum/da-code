import pandas as pd
from scipy import stats

# Load the data for men's and women's results
men_results = pd.read_csv('men_results.csv')
women_results = pd.read_csv('women_results.csv')

# Calculate the total goals for each match
men_goals = men_results['home_score'] + men_results['away_score']
women_goals = women_results['home_score'] + women_results['away_score']

# Perform a two-sample t-test
t_stat, p_value = stats.ttest_ind(men_goals, women_goals, equal_var=False)

# Determine whether to reject the null hypothesis using a 10% significance level
alpha = 0.10
hypothesis_result = 'reject' if p_value < alpha else 'fail to reject'

# Save the result to 'result.csv'
result = pd.DataFrame({
    't_stat': [t_stat],
    'p_value': [p_value],
    'hypothesis_result': [hypothesis_result]
})
result.to_csv('result.csv', index=False)

print(result)
