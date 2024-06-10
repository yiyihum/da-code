import pandas as pd

# Load the matches data
matches = pd.read_csv('matches.csv')

# Count the number of matches played by each team
team_matches = matches['team1'].value_counts() + matches['team2'].value_counts()

# Filter out teams that have participated in more than 100 matches
teams_more_than_100 = team_matches[team_matches > 100].index.tolist()

# Output the teams that have played more than 100 matches
print(teams_more_than_100)
