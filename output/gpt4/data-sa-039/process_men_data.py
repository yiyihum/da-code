import pandas as pd

# Load the Excel file
men_results_path = 'men_results.xls'
men_results = pd.read_excel(men_results_path)

# Filter for matches from 2002 onwards
men_results['date'] = pd.to_datetime(men_results['date'])
men_results_filtered = men_results[men_results['date'].dt.year >= 2002]

# Calculate the total goals scored in each match using .loc to avoid SettingWithCopyWarning
men_results_filtered.loc[:, 'total_goals'] = men_results_filtered['home_score'] + men_results_filtered['away_score']

# Extract the total goals as a list for the Mann-Whitney U test
men_goals = men_results_filtered['total_goals'].tolist()

# Save the processed data to a new CSV file for later use
men_results_filtered.to_csv('/workspace/men_goals.csv', index=False)

# Output the total goals to verify the processing
print(men_goals[:5])
