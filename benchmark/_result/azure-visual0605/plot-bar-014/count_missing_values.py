import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/synthetic_automobile_crash_data_india.csv')

# Count the missing values for each feature
missing_values_count = df.isnull().sum()

# Filter out features with no missing values and sort the rest in descending order
missing_values_count = missing_values_count[missing_values_count > 0].sort_values(ascending=False)

# Create a bar chart for the features with missing values
plt.figure(figsize=(8, 6))
missing_values_count.plot(kind='bar')
plt.title('Feature Missing Values Count')
plt.xlabel('Features')
plt.ylabel('Missing Values Count')
plt.xticks(rotation=45, ha='right')

# Save the chart as output.png
plt.savefig('/workspace/output.png', bbox_inches='tight')
