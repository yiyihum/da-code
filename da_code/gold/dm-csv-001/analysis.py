import pandas as pd
import numpy as np

dataframe = pd.read_csv("../ufc-fighters-statistics.csv")
df = dataframe.copy() 

conditions = [
    (df['weight_in_kg'].isna()),
    (df['weight_in_kg'] <= 57.0), 
    (df['weight_in_kg'] > 57.0) & (df['weight_in_kg'] <= 61.2),
    (df['weight_in_kg'] > 61.2) & (df['weight_in_kg'] <= 65.8),
    (df['weight_in_kg'] > 65.8) & (df['weight_in_kg'] <= 70.0),
    (df['weight_in_kg'] > 70.0) & (df['weight_in_kg'] <= 77.1),
    (df['weight_in_kg'] > 77.1) & (df['weight_in_kg'] <= 83.9),
    (df['weight_in_kg'] > 83.9) & (df['weight_in_kg'] <= 93.0),
    (df['weight_in_kg'] > 93.0)
    ]

level = ['Not know', 'Flyweight', 'Bantamweight', 'Featherweight',
         'Lightweight','Welterweight','Middleweight','Light Heavyweight','Heavyweight']


df['Weight_class'] = np.select(conditions, level)


weight_cat_list = set(df["Weight_class"].values)

df["matches_played"] = df["wins"] + df["losses"] + df["draws"]
df["win_perc"] = round((df["wins"] / df["matches_played"]),2) * 100

output_num = []
for cat in level:
    data_of_cat = df.loc[df["Weight_class"] == cat]
    num_of_undefeated = len(data_of_cat[(data_of_cat['win_perc'] == 100)])
    output_num.append(num_of_undefeated)


file_path = 'undefeated.csv'
def append_data_to_csv(file_path, levels, fighter_nums):
    df = pd.DataFrame({
        'level': levels,
        'fighter_num': fighter_nums
    })
    df.to_csv(file_path, mode='a', header=False, index=False)
    print(f"Data appended to {file_path}")

append_data_to_csv(file_path, level, output_num)