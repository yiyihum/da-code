import pandas as pd
import numpy as np 
from scipy import stats

import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv('../all_seasons.csv', index_col=0)
country_codes = pd.read_csv("../country_code.csv", index_col=0)
categoricals = df.select_dtypes(exclude=[np.number])
country_codes = country_codes[['Country_name', 'code_3digit']]
country_codes = country_codes.rename({'Country_name': 'country'}, axis=1) 
country_codes['country'] = country_codes['country'].replace({'United States of America': 'USA', 'Russian Federation':'Russia',
                                                             'Venezuela (Bolivarian Republic)':'Venezuela', 'Korea (South)':'South Korea',
                                                             'Tanzania, United Republic of':'Tanzania','Macedonia, Republic of':'Macedonia',
                                                             'Congo, (Kinshasa)':'Democratic Republic of the Congo',
                                                             'Congo (Brazzaville)':'Congo','Iran, Islamic Republic of':'Iran',
                                                             'Virgin Islands, US':'US Virgin Islands',
                                                             })
# Create drafted column wiht boolean logic
df['drafted'] = np.where(df['draft_year'] != 'Undrafted', 1, 0)
# Convert draft_year column into a date type
# Replace Undrafted with NaN
df['draft_year'] = df['draft_year'].replace(r'Undrafted', np.nan, regex=True)
# Convert the column data type to date
df['draft_year'] = pd.to_datetime(df['draft_year'])
df['season'] = pd.to_datetime(df['season'].str[:4])
df['country'] = df['country'].replace({'Great Britain':'United Kingdom','England':'United Kingdom','Scotland':'United Kingdom',
                                       'Bosnia & Herzegovina':'Bosnia and Herzegovina','Bosnia':'Bosnia and Herzegovina',
                                       'Cabo Verde':'Cape Verde','St. Vincent & Grenadines':'Saint Vincent and Grenadines'})
main_variables = df.groupby('player_name', as_index=False).agg({'player_height': 'mean', 'player_weight':'mean'})

df['bmi'] = df['player_weight'].values / (df['player_height'].values ** 2) * 10000

plt.figure(figsize=(16, 8))
sns.lineplot(x=df['season'], y='bmi', data=df, marker="o", ci=None, color='#17408b')
plt.title('Average BMI Each Season', fontsize=22)
plt.ylabel('BMI')
plt.xlabel('Season')
sns.despine()

plt.show()