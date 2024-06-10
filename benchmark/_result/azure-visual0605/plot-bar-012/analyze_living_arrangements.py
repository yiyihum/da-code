import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/student-mat.csv')

# Define the age groups
teenagers = df[(df['age'] >= 15) & (df['age'] <= 17)]
adults = df[df['age'] >= 18]

# Count living arrangements for teenagers
teenagers_living_together = teenagers[teenagers['Pstatus'] == 'T'].shape[0]
teenagers_living_apart = teenagers[teenagers['Pstatus'] == 'A'].shape[0]

# Count living arrangements for adults
adults_living_together = adults[adults['Pstatus'] == 'T'].shape[0]
adults_living_apart = adults[adults['Pstatus'] == 'A'].shape[0]

# Data for plotting
ages = ['Teenagers', 'Adults']
living_together = [teenagers_living_together, adults_living_together]
living_apart = [teenagers_living_apart, adults_living_apart]

# Plotting the bar chart
fig, ax = plt.subplots(figsize=(15, 10))
bar_width = 0.35
index = range(len(ages))

bar1 = ax.bar(index, living_together, bar_width, label='Living Together')
bar2 = ax.bar([i + bar_width for i in index], living_apart, bar_width, label='Living Apart')

ax.set_xlabel('Living Together Sum and Living Apart Sum')
ax.set_ylabel('Age')
ax.set_title('Where do children between 15 and 22 live')
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(ages)
ax.legend()

# Save the figure
plt.savefig('/workspace/result.png')
