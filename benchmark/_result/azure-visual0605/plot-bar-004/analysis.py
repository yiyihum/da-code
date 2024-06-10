import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data_raw = pd.read_csv('train.csv')

# Filter out the survivors
survivors = data_raw[data_raw['Survived'] == 1]

# Create a bar plot for the number of male and female survivors in each passenger class
plt.figure(figsize=(14, 12))
sns.countplot(x='Sex', hue='Pclass', data=survivors, palette=["#e9d4d0", "#a16f8d", "#2d223a"])

# Set the title and labels
plt.title('Sex vs Pclass Survival Comparison')
plt.xlabel('Sex')
plt.ylabel('Survived')

# Save the plot as 'result.jpg'
plt.savefig('result.jpg')
