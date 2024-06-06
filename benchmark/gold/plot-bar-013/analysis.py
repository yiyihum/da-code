#importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('../icc hall of fame.csv')

# Display the first few rows of the dataframe
print("First few rows of the dataset:")
print(df.head())

# Data cleanup: Convert 'Induction' to integer if it's not and parse 'dob' as datetime
df['Induction'] = pd.to_numeric(df['Induction'], errors='coerce')
df['dob'] = pd.to_datetime(df['dob'], format='%Y-%m-%d', errors='coerce')

# Explore the distribution of roles
plt.figure(figsize=(12, 6))
sns.countplot(x='role', data=df)
plt.title('Distribution of Player Roles in Hall of Fame')
plt.xlabel('Player Role')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.show()