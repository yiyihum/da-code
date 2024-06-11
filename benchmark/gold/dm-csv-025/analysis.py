import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import math
from decimal import Decimal
warnings.filterwarnings("ignore")

ball_by_ball_data = pd.read_csv("../IPL Ball-by-Ball 2008-2020.csv")
match_data = pd.read_csv("../IPL Matches 2008-2020.csv")

# Rename Rising Pune Supergiant as Rising Pune Supergiants
match_data['team1'] = match_data['team1'].apply(lambda x : 'Rising Pune Supergiants' if x == 'Rising Pune Supergiant' else x)
match_data['team2'] = match_data['team2'].apply(lambda x : 'Rising Pune Supergiants' if x == 'Rising Pune Supergiant' else x)
match_data['winner'] = match_data['winner'].apply(lambda x : 'Rising Pune Supergiants' if x == 'Rising Pune Supergiant' else x)
match_data['toss_winner'] = match_data['toss_winner'].apply(lambda x : 'Rising Pune Supergiants' if x == 'Rising Pune Supergiant' else x)

# Lets calculate the winning probability of each team
def winning_probability(team):    
    # Extract the data for the given team
    team_data = match_data[(match_data['team1'] == team) | (match_data['team2'] == team)]
    # Calculate the total number of matches played, won and lost
    total_matches_played = team_data.shape[0]
    total_matches_won = team_data[team_data['winner'] == team].shape[0]
    total_matches_lost = team_data[team_data['winner'] != team].shape[0]
    # Calculate the winning and losing probability
    '''
    Here, the winning and losing probabilities is taken as follows:
    
    Winning Probability = Total Matches Won/ Total Matches Playes
    Losing Probability = Total Matches Lost/ Total Matches Played 
    '''
    winning_probability = total_matches_won/total_matches_played
    losing_probability = total_matches_lost/total_matches_played
     
    return winning_probability, losing_probability

# Calculate the Winning and Losing Probability Distribution for each team and plot the binomial distributions for 50 Matches
IPL_teams = match_data['team1'].unique().tolist()

# Dictionary to store the winning and losing probabilities for a given team
winning_probability_map = {}
losing_probability_map = {}

for team in IPL_teams:
    team_win_prob, team_lose_prob = winning_probability(team)
    winning_probability_map[team] = team_win_prob
    losing_probability_map[team] = team_lose_prob

sorted_win_probs = sorted(winning_probability_map.values(), reverse=True)
sorted_lose_probs = sorted(losing_probability_map.values(), reverse=True)

# Convert the sorted lists to numpy arrays
win_array = np.array(sorted_win_probs)
lose_array = np.array(sorted_lose_probs)

print(win_array, lose_array)
# Save the numpy arrays to .npy files
np.save('win.npy', win_array)
np.save('lose.npy', lose_array)

# Find the team with the highest winning probability
team_with_highest_win_prob = max(winning_probability_map, key=winning_probability_map.get)
highest_win_prob = winning_probability_map[team_with_highest_win_prob]

# Find the team with the highest losing probability
team_with_highest_lose_prob = max(losing_probability_map, key=losing_probability_map.get)
highest_lose_prob = losing_probability_map[team_with_highest_lose_prob]

print(f"Team with the highest winning probability: {team_with_highest_win_prob} with probability {highest_win_prob}")
print(f"Team with the highest losing probability: {team_with_highest_lose_prob} with probability {highest_lose_prob}")

# Save the results to a .csv file
results = pd.DataFrame({
    'Team': [team_with_highest_win_prob, team_with_highest_lose_prob],
    'Probability': [highest_win_prob, highest_lose_prob],
    'Type': ['Winning', 'Losing']
})

results.to_csv('team_probabilities.csv', index=False)