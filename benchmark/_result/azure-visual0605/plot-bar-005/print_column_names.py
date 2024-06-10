import pandas as pd

# Load the survey data
df = pd.read_csv('multipleChoiceResponses.csv', low_memory=False)

# Print all column names to identify the age column
print(df.columns.tolist())
