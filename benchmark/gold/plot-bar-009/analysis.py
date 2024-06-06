import pandas as pd
import numpy as np # data pre-processing
import matplotlib.pyplot as plt

df_athletes = pd.read_excel("../Athletes.xlsx")
df_coaches = pd.read_excel("../Coaches.xlsx")
df_entries_gender = pd.read_excel("../EntriesGender.xlsx")
df_medals = pd.read_excel("../Medals.xlsx")
df_teams = pd.read_excel("../Teams.xlsx")

x = df_athletes.NOC.value_counts()
countries = x.index[:10].values
coaches = [x.loc[country] for country in countries]

gold = [df_medals[df_medals['Team/NOC'] == country]["Gold"].values[0] for country in countries]

bar_width = 0.35
index = np.arange(len(countries))

fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(index, coaches, bar_width, label='Coaches')
bars2 = ax.bar(index + bar_width, gold, bar_width, label='Gold Medals')

ax.set_xlabel('Countries')
ax.set_ylabel('Count')
ax.set_title('Number of Coaches and Gold Medals by Country')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(countries, rotation=30)
ax.legend()

plt.tight_layout()
plt.savefig('./result.png')