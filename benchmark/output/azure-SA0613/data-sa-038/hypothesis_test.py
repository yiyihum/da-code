import pandas as pd
from scipy import stats

# Load the datasets
men_df = pd.read_csv('men_results.csv')
women_df = pd.read_csv('women_results.csv')

# Calculate the total goals for each match
men_df['total_goals'] = men_df['home_score'] + men_df['away_score']
women_df['total_goals'] = women_df['home_score'] + women_df['away_score']

# Perform a two-sample t-test
t_stat, p_val = stats.ttest_ind(men_df['total_goals'], women_df['total_goals'], equal_var=False)

# Determine the result based on a 10% significance level
result = 'reject' if p_val < 0.10 else 'fail to reject'

# Save the results to result.csv
result_df = pd.DataFrame({'p_val': [p_val], 'result': [result]})
result_df.to_csv('result.csv', index=False)
