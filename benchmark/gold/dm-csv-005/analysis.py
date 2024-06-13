import pandas as pd

# Load the Users.csv file
users_df = pd.read_csv('../Users.csv')
users_df["Age"] = users_df["Age"].fillna(30)
# Define the age groups based on age.txt
age_groups = {
    'child': (0, 13),
    'teenager': (14, 19),
    'young': (20, 25),
    'adult': (26, 65),
    'old': (66, 300)
}

# Initialize a dictionary to hold the count for each age group
age_group_counts = {age_group: 0 for age_group in age_groups}

# Function to categorize age into age groups
def categorize_age(age):
    for group, (start, end) in age_groups.items():
        if start <= age <= end:
            return group
    return None

# Count the number of users in each age group
for age in users_df['Age'].dropna():
    group = categorize_age(age)
    if group:
        age_group_counts[group] += 1

# Save the results to a CSV file
result_df = pd.DataFrame(list(age_group_counts.items()), columns=['Age', 'total'])
result_df.to_csv('./result.csv', index=False)
