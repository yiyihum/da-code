import pandas as pd

# Read the dataset with low_memory=False to avoid DtypeWarning
df = pd.read_csv('multipleChoiceResponses.csv', low_memory=False)

# Print out the first few rows to identify the age column
print(df.head())
