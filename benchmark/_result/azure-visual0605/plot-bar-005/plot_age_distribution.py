import pandas as pd
import matplotlib.pyplot as plt

# Load the survey data
df = pd.read_csv('multipleChoiceResponses.csv', skiprows=[1], low_memory=False)

# Count the number of respondents in each age group
age_group_counts = df['Q2'].value_counts().sort_index()

# Plot the bar chart
plt.figure(figsize=(10, 6))
age_group_counts.plot(kind='bar')
plt.title('Age Group Distribution')
plt.xlabel('Age Group')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plotted bar chart as 'result.png'
plt.savefig('result.png')
