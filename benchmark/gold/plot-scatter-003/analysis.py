import pandas as pd 
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

athlete_events_df = pd.read_csv("../athlete_events.csv")
noc_regions_df = pd.read_csv("../noc_regions.csv")

def missing_data(data):
    total = data.isnull().sum().sort_values(ascending = False)
    percent = (data.isnull().sum()/data.isnull().count()*100).sort_values(ascending = False)
    return pd.concat([total, percent], axis=1, keys=['Total', 'Percent'])
missing_data(athlete_events_df)

tmp = athlete_events_df.groupby(['Year', 'City'])['Season'].value_counts()
df = pd.DataFrame(data={'Athlets': tmp.values}, index=tmp.index).reset_index()

plt.figure(figsize=(12, 8))
plt.scatter(df['Year'], df['Athlets'], color='blue')
plt.title('Athlets per Olympic game')
plt.xlabel('Year')
plt.ylabel('Number of athlets')
plt.yticks([0, 2000, 4000, 6000, 8000, 10000, 12000], ['0', '2k', '4k', '6k', '8k', '10k', '12k'])
plt.show()
