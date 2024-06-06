import pandas as pd
import matplotlib.pyplot as plt

deliveries = pd.read_csv('../deliveries.csv')

v_kohli = deliveries[deliveries['batter'] == 'V Kohli']

labels = v_kohli['batsman_runs'].unique()
labels = labels[labels != 0].tolist()

values = []
for value in [1, 2, 3, 4, 6]:
    length = len(v_kohli[v_kohli['batsman_runs'] == value]) * value
    values.append(length)

fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)

ax.legend(wedges, labels, title="Runs", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

ax.set_title('Distribution of Batsman Runs for V Kohli')

plt.savefig('./distribution.png')

plt.show()
