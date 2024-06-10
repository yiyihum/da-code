import pandas as pd

# Load the survey data
df = pd.read_csv('multipleChoiceResponses.csv', low_memory=False)

# Print the first few rows of the dataframe to identify the age column
print(df.head())
