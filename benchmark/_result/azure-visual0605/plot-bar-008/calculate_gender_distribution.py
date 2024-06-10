import pandas as pd
import matplotlib.pyplot as plt

# Load the processed data
df = pd.read_csv('/workspace/processed_survey_data.csv')

# Calculate the gender distribution for each country
gender_distribution = df.groupby(['Q3', 'Q1']).size().unstack().fillna(0)

# Calculate the percentage distribution
gender_distribution_percentage = gender_distribution.div(gender_distribution.sum(axis=1), axis=0) * 100

# Plot the bar chart
fig, ax = plt.subplots(figsize=(16, 8))
gender_distribution_percentage.plot(kind='bar', stacked=True, ax=ax)

# Set the chart title and labels
ax.set_title('Country-wise Gender Distribution')
ax.set_xlabel('Country')
ax.set_ylabel('Percentage')

# Save the chart
plt.savefig('/workspace/distribution.png')
