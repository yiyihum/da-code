import pandas as pd

df_summer = pd.read_csv('../Athletes_summer_games.csv')
df_winter = pd.read_csv('../Athletes_winter_games.csv')

df_sum_win = pd.concat([df_summer, df_winter])

# Total Number of Olympics held to date
total_games = pd.DataFrame(columns=['Total # of Games'])
total_games.loc['Winter'] = len(df_winter['Games'].drop_duplicates())
total_games.loc['Summer'] = len(df_summer['Games'].drop_duplicates())

total_games = total_games.reset_index().rename(columns={'index':'Season'})
total_games_path = './allGames.csv'
total_games.to_csv(total_games_path, index=False)
print(f'Total games have been saved in {total_games_path}')

# Total Number of Events Per Game
df_all_events = pd.concat([df_winter[['Games', 'Year', 'City', 'Event']], df_summer[['Games', 'Year', 'City', 'Event']]])

games_list = df_all_events['Games'].drop_duplicates().to_list()
games_list_num = []

for e in games_list:
    games_list_num.append(pd.DataFrame(df_all_events[df_all_events['Games'] == e].drop_duplicates()).shape[0])

total_events = pd.DataFrame(columns=[['Games', 'Year', 'City', 'Total # of Events']])
total_events['Games'] = games_list
total_events['Total # of Events'] = games_list_num
games_years = df_all_events[['Games', 'Year', 'City']].drop_duplicates(subset='Games').reset_index(drop=True)
total_events[['Year', 'City']] = games_years[['Year', 'City']]
total_events_path = './allEvents.csv'
total_events.to_csv(total_events_path, index=False)
print(f'Total events have been saved in {total_events_path}')

