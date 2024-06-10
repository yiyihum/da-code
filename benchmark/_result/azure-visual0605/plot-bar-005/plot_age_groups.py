import pandas as pd
import matplotlib.pyplot as plt

# Read the survey data
df = pd.read_csv('multipleChoiceResponses.csv', low_memory=False)

# The column containing age information needs to be identified
age_column = None
for column in df.columns:
    if 'age' in column.lower():
        age_column = column
        break

# Check if the age column was found
if age_column is None:
    raise ValueError("No age column found in the survey data.")

# Define the age groups
age_groups = {
    '18-21': (18, 21),
    '22-24': (22, 24),
    '25-29': (25, 29),
    '30-34': (30, 34),
    '35-39': (35, 39),
    '40-44': (40, 44),
    '45-49': (45, 49),
    '50-54': (50, 54),
    '55-59': (55, 59),
    '60-69': (60, 69),
    '70-79': (70, 79),
    '80+': (80, float('inf')),
}

# Initialize a dictionary to count the number of people in each age group
age_group_counts = {group: 0 for group in age_groups}

# Process the data to count the number of respondents in each age group
for age in df[age_column].dropna():
    for group, (start_age, end_age) in age_groups.items():
        if start_age <= age <= end_age:
            age_group_counts[group] += 1
            break

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(age_group_counts.keys(), age_group_counts.values())
plt.title('Age Group Distribution')
plt.xlabel('Age Group')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plotted bar chart as 'result.png'
plt.savefig('result.png')
