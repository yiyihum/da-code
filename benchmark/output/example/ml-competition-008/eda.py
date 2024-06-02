import pandas as pd
import matplotlib.pyplot as plt

# Load the train.csv file into a pandas dataframe
train_df = pd.read_csv('train.csv')

# Plot the distribution of the target variable 'FloodProbability'
plt.figure(figsize=(10, 6))
plt.hist(train_df['FloodProbability'], bins=30, edgecolor='black')
plt.title('Distribution of Flood Probability')
plt.xlabel('Flood Probability')
plt.ylabel('Frequency')
plt.show()

# Calculate the correlation between the features and the target variable
correlation = train_df.corr()['FloodProbability'].sort_values()

# Print the correlation
print(correlation)
