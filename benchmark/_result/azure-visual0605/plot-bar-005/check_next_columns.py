import pandas as pd

# Load the survey data
df = pd.read_csv('multipleChoiceResponses.csv', low_memory=False)

# Check the unique values in the next few columns to identify the age column
for column in ['Q2', 'Q3', 'Q4', 'Q5']:
    print(f"Unique values in {column}:")
    print(df[column].unique())
    print("\n")
