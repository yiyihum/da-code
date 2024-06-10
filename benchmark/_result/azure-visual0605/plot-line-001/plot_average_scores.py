import pandas as pd
import matplotlib.pyplot as plt

# Load the game data
df = pd.read_csv('game.csv')

# Convert game_date to datetime and extract the year
df['game_year'] = pd.to_datetime(df['game_date']).dt.year

# Calculate the total points for each game
df['total_points'] = df['pts_home'] + df['pts_away']

# Group by the game year and calculate the average total points
average_points_per_year = df.groupby('game_year')['total_points'].mean().reset_index()
average_points_per_year.rename(columns={'total_points': 'average_points'}, inplace=True)

# Plot the line graph
plt.figure(figsize=(10, 5))
plt.plot(average_points_per_year['game_year'], average_points_per_year['average_points'], color='blue')
plt.title('NBA: Average Total Points per Game')
plt.xlabel('game_year')
plt.ylabel('average_points')
plt.savefig('points_graph.png')
plt.close()
