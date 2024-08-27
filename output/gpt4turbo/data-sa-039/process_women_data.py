import pandas as pd

# Load the CSV file
women_results_path = 'women_results.csv'
women_results = pd.read_csv(women_results_path)

# Filter for matches from 2002 onwards
women_results['date'] = pd.to_datetime(women_results['date'])
women_results_filtered = women_results[women_results['date'].dt.year >= 2002]

# Calculate the total goals scored in each match
women_results_filtered['total_goals'] = women_results_filtered['home_score'] + women_results_filtered['away_score']

# Extract the total goals as a list for the Mann-Whitney U test
women_goals = women_results_filtered['total_goals'].tolist()

# Save the processed data to a new CSV file for later use
women_results_filtered.to_csv('/workspace/women_goals.csv', index=False)

# Output the total goals to verify the processing
print(women_goals[:5])
