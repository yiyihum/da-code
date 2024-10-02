import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

df1 =pd.read_csv('../athlete_events.csv')
regions = pd.read_csv('../noc_regions.csv')

df_china=df1.loc[(df1['Team']=='China')]
df_china_medal=df_china.loc[df_china['Medal']=='Gold']

medal_map = {'Gold':1}
df_china_medal['Medal'] = df_china_medal['Medal'].map(medal_map)

df_china_sport=df_china_medal.groupby(['Sport'],as_index=False)['Medal'].agg('sum')

df_china_sport=df_china_sport.sort_values(['Medal'],ascending=False)

df_china_sport=df_china_sport.head(10)

temp_series = df_china_sport['Medal']
labels = df_china_sport['Sport']
sizes = (np.array((temp_series / temp_series.sum())*100))
print(labels)
print(sizes)


