import pandas as pd
import matplotlib.pyplot as plt

# Read the dataset
df = pd.read_csv('multipleChoiceResponses.csv', low_memory=False)

# Assuming the age column is labeled 'Q1'
age_column = 'Q1'
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

# Function to categorize age
def categorize_age(age):
    if pd.isnull(age) or age == 'Prefer not to say':
        return None
    try:
        age = int(age)
    except ValueError:
        return None
    for group, (start, end) in age_groups.items():
        if start <= age <= end:
            return group
    return None

# Process the age data
for age in df[age_column]:
    group = categorize_age(age)
    if group:
        age_group_counts[group] += 1

# Plot the bar chart
plt.figure(figsize=(10, 6))
plt.bar(age_group_counts.keys(), age_group_counts.values(), color='skyblue')
plt.title('Age Group Distribution')
plt.xlabel('Age Group')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('result.png')
