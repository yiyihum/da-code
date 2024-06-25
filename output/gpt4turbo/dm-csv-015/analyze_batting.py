import pandas as pd

# Load the batting data
batting_df = pd.read_csv('batting.csv')

# Find the top players in the specified categories
most_games_played = batting_df.loc[batting_df['g'].idxmax()]
most_runs = batting_df.loc[batting_df['r'].idxmax()]
most_hits = batting_df.loc[batting_df['h'].idxmax()]
most_home_runs = batting_df.loc[batting_df['hr'].idxmax()]

# Create a DataFrame to store the results
result_df = pd.DataFrame({
    'job title': [
        'Most Games Played',
        'Most Runs',
        'Most Hits',
        'Most Home Runs'
    ],
    'Player_Name': [
        most_games_played['player_id'],
        most_runs['player_id'],
        most_hits['player_id'],
        most_home_runs['player_id']
    ],
    'Batting_Table_Topper': [
        most_games_played['g'],
        most_runs['r'],
        most_hits['h'],
        most_home_runs['hr']
    ]
})

# Save the results to a CSV file
result_df.to_csv('result.csv', index=False)
