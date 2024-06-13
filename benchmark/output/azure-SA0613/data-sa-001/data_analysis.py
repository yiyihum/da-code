import pandas as pd
from scipy.stats import mannwhitneyu

# Load the datasets
men_df = pd.read_csv('men_results.csv')
women_df = pd.read_csv('women_results.csv')

# Filter for World Cup matches since 2000
men_world_cup = men_df[(men_df['tournament'] == 'FIFA World Cup') & (pd.to_datetime(men_df['date']).dt.year >= 2000)]
women_world_cup = women_df[(women_df['tournament'] == 'FIFA World Cup') & (pd.to_datetime(women_df['date']).dt.year >= 2000)]

# Calculate the total number of goals in each match
men_goals = men_world_cup['home_score'] + men_world_cup['away_score']
women_goals = women_world_cup['home_score'] + women_world_cup['away_score']

# Perform the Mann-Whitney U test
u_stat, p_val = mannwhitneyu(women_goals, men_goals, alternative='greater')

# Determine the result based on the p-value
result = 'reject' if p_val < 0.01 else 'fail to reject'

# Save the results to a CSV file
results_df = pd.DataFrame({'p_val': [p_val], 'result': [result]})
results_df.to_csv('/workspace/result.csv', index=False)
