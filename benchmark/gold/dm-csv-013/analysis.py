import numpy as np 
import pandas as pd 


df_read=pd.read_csv("../players_20.csv")
df_read["BMI"]=df_read['weight_kg'] / (df_read['height_cm'] / 100) ** 2
df1 = df_read[['short_name','age','dob','height_cm','weight_kg','nationality','club','overall','potential',
          'value_eur','wage_eur','player_positions','preferred_foot','international_reputation',
          'skill_moves', 'work_rate',"BMI"]]
top_clubs = df1.groupby(['club']).overall.mean().sort_values(ascending  = False)[:20]
top_clubs_list = top_clubs.index.tolist()
average_bmi_by_club = df1[df1['club'].isin(top_clubs_list)].groupby('club')['BMI'].mean()
best_club = average_bmi_by_club.idxmin()

best_club_players = df_read[df_read['club'] == best_club]
best_shooter = best_club_players.loc[best_club_players['shooting'].idxmax()]

data = {'club': [best_club], 'best_shooter': [best_shooter['long_name']]}
df = pd.DataFrame(data)
df.to_excel('./result.xlsx', index=False)