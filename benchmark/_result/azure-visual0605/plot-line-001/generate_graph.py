import pandas as pd
import matplotlib.pyplot as plt

# Load the game data
game_data = pd.read_csv('game.csv', parse_dates=['game_date'])

# Calculate the average points per game
game_data['avg_points'] = (game_data['pts_home'] + game_data['pts_away']) / 2

# Group by game_date and calculate the mean of avg_points
average_scores = game_data.groupby('game_date')['avg_points'].mean().reset_index()

# Plot the line graph
plt.figure(figsize=(10, 5))
plt.plot(average_scores['game_date'], average_scores['avg_points'], label='Average Game Score')
plt.xlabel('Game Date')
plt.ylabel('Average Score')
plt.title('Average NBA Game Scores Over Time')
plt.legend()
plt.tight_layout()

# Save the graph as 'points.png'
plt.savefig('points.png')
