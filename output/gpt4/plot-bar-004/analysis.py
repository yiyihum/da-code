import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read data from file
data_raw = pd.read_csv('./train.csv')

# Set style for seaborn
sns.set(style="whitegrid")

# Create the plot
plt.figure(figsize=[14, 12])
ax = sns.countplot(x='Sex', hue='Pclass', data=data_raw)

# Set the title and labels
ax.set_title("Sex vs Pclass Survival Comparison")
ax.set_xlabel("Sex")
ax.set_ylabel("Survived")
ax.legend(title="Pclass")

# Set legend labels
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles=handles, labels=["1", "2", "3"], title="Pclass")

# Set xtick labels
ax.set_xticklabels(["male", "female"])

# Save the figure
plt.savefig('result.png')
