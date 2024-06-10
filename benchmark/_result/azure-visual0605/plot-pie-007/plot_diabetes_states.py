import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('diabetes_012_health_indicators_BRFSS2015.csv')

# Count the occurrences of each category in the 'Diabetes_012' column
category_counts = df['Diabetes_012'].value_counts(normalize=True)

# Define the labels and colors for the pie chart
labels = ['Healthy', 'Pre-Diabetic', 'Diabetic']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# Plot the pie chart
plt.figure(figsize=(8, 8))
plt.pie(category_counts, labels=labels, colors=colors, autopct='%1.1f%%')
plt.title('Proportion of Different Diabetes States')
plt.savefig('result.png')
