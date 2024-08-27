import pandas as pd

# Load the dataset
df = pd.read_csv('ds_salaries.csv')

# Count the frequency of each experience level
experience_level_counts = df['experience_level'].value_counts()

# Find the most frequent experience level
most_frequent_experience_level = experience_level_counts.idxmax()
most_frequent_count = experience_level_counts.max()

# Calculate the ratio
total_counts = experience_level_counts.sum()
ratio = most_frequent_count / total_counts

# Output the result in JSON format
result = {
    "The most frequent experience level": [most_frequent_experience_level],
    "ratio": [ratio]
}

# Print the result
print(result)
