import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)

df = pd.read_csv('../game.csv', parse_dates=['game_date'])

df_games = df[df['season_type'].isin(['Regular Season', 'Playoffs'])]
df_games = df_games.loc[:, ['game_date', 'pts_home', 'pts_away', 'fg3m_home', 'fg3a_home', 'fg3m_away', 'fg3a_away']]
df_games.insert(0, 'game_year', df_games['game_date'].dt.year)
df_games = df_games.drop('game_date', axis=1)

df_games.insert(3, 'total_score', df_games['pts_home'] + df_games['pts_away'])
df_games = df_games.drop(['pts_home', 'pts_away'], axis=1)

df_games['fg3_made'] = df_games['fg3m_home'] + df_games['fg3m_away']
df_games['fg3_attempts'] = df_games['fg3a_home'] + df_games['fg3a_away']
df_games['fg3_pct'] = df_games['fg3_made'] / df_games['fg3_attempts']

df_games = df_games.drop(['fg3m_home', 'fg3m_away', 'fg3a_home', 'fg3a_away'], axis=1)
df_games.sort_values('fg3_pct', ascending=False)
# Dropping Invalid Data
df_games.query('fg3_attempts < fg3_made')
df_games = df_games.drop(df_games.query('fg3_attempts < fg3_made').index)
df_games.sort_values('fg3_pct', ascending=False)
plt.figure()
df_years = df_games.groupby('game_year')['total_score'].mean()
df_years.plot(title='NBA: Average Total Points per Game')
plt.savefig('./points_graph.png')
