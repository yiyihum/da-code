import pandas as pd

# Load the survey data
df = pd.read_csv('multipleChoiceResponses.csv', low_memory=False)

# Check the unique values in the "Q1" column to confirm if it contains age data
age_data = df['Q1'].unique()
print(age_data)
