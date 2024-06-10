import pandas as pd
import matplotlib.pyplot as plt

# Load the results dataset
results_df = pd.read_csv('/workspace/results.csv')

# Filter the data for matches between 2000 and 2023
filtered_df = results_df[(results_df['date'] >= '2000-01-01') & (results_df['date'] <= '2023-12-31')]

# Group by home team and calculate the required statistics
grouped = filtered_df.groupby('home_team').agg(
    average_home_score=('home_score', 'mean'),
    average_away_score=('away_score', 'mean'),
    matches_played=('date', 'count'),
    neutral_ground_matches=('neutral', lambda x: x.sum())
)

# Calculate the overall score for each team
grouped['overall_score'] = grouped['matches_played'] + 2 * grouped['neutral_ground_matches']

# Sort the teams by overall score in descending order and get the top 10
top_teams = grouped.sort_values(by='overall_score', ascending=False).head(10)

# Create a bar chart
plt.figure(figsize=(12, 8))
plt.bar(top_teams.index, top_teams['overall_score'])
plt.title('Best Teams from 2000 to 2023')
plt.xlabel('Football Team')
plt.ylabel('Overall Score')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the bar chart as 'team.png'
plt.savefig('/workspace/team.png')
