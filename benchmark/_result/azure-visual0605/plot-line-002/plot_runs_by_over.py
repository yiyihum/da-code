import pandas as pd
import matplotlib.pyplot as plt

# Load the deliveries data
deliveries = pd.read_csv('deliveries.csv')

# Dictionary of teams and their abbreviations
team_abbreviations = {
    'Mumbai Indians': 'MI',
    'Kolkata Knight Riders': 'KKR',
    'Royal Challengers Bangalore': 'RCB',
    'Deccan Chargers': 'DC',
    'Chennai Super Kings': 'CSK',
    'Rajasthan Royals': 'RR',
    'Delhi Daredevils': 'DD',
    'Kings XI Punjab': 'KXIP'
}

# Filter out the teams that have played more than 100 matches
teams_more_than_100 = ['Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab',
                       'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals',
                       'Royal Challengers Bangalore']

# Replace full team names with abbreviations in the deliveries dataframe
deliveries.replace(team_abbreviations, inplace=True)

# Filter the deliveries to include only the teams that have played more than 100 matches
deliveries_filtered = deliveries[deliveries['batting_team'].isin(teams_more_than_100)]

# Group by over and batting team, and sum the total runs
runs_by_over = deliveries_filtered.groupby(['over', 'batting_team'])['total_runs'].sum().unstack()

# Plot the line graph
plt.figure(figsize=(15, 8))
for team in runs_by_over.columns:
    plt.plot(runs_by_over.index, runs_by_over[team], label=team)

plt.xlabel('Over')
plt.ylabel('Total Runs Scored')
plt.title('Total Runs Scored by Each Team in Each Over')
plt.legend()
plt.grid(True)
plt.savefig('result.png')
