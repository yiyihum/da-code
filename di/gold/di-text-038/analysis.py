# Setup Code Block
import numpy as np
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
print("Setup Complete")


#Read the CSVs and prepare the data
players_data = pd.read_csv("../players.csv",index_col=0)
stats_data = pd.read_csv("../stats.csv")
#Since we're only concerned about 2021 stats, we'll filter it out
stats_data_main = stats_data.loc[stats_data.year == 2021]
stats_data_main = stats_data_main.rename(columns={'Goal Assists': 'Assists'})
#Combine the two CSVs to only reference one in the entire session
left = players_data
right = stats_data_main.set_index('playerId')
filtered_player_df = right.join(left, lsuffix='_PD', rsuffix='_SD')

## We need a New Dataframe containing the total goals for 2021 per player and their positions
#Get the total goals for 2021 for each player
total_goals_series = filtered_player_df.groupby('playerId').Goals.sum().sort_index(ascending=False)
total_assists_series = filtered_player_df.groupby('playerId').Assists.sum().sort_index(ascending=False)

#Get unique index list
sorted_index = filtered_player_df.index.unique().values
sorted_index[::-1].sort()

#Replace all dual positions and get position series
def replace_dual_positions(row):
    row.position = (row.position.split(","))[0]
    return row

edited_pos_df = players_data.apply(replace_dual_positions, axis='columns').sort_index(ascending=False)
filtered_edited_pos = edited_pos_df.loc[np.isin(edited_pos_df.index.values,sorted_index)].sort_index(ascending=False)
pos_series = filtered_edited_pos['position']
pos_series

#Create Data Frame for Visualizations
viz_df = pd.DataFrame({ 'total_goals':total_goals_series,
        'positions': pos_series,
        'total_assists': total_assists_series
    },index = sorted_index)
viz_df.total_goals.fillna(0, inplace=True)
viz_df.total_assists.fillna(0, inplace = True)
viz_df = viz_df.astype({"total_goals": int, "total_assists" : int})

plt.figure(figsize=(20,8))
sns.set_style("dark")
plt.title("Distribution of Total Goals (per Player) for 2021, by Position")
sns.kdeplot(data=viz_df, x='total_goals', hue='positions', shade=True, palette = "colorblind")