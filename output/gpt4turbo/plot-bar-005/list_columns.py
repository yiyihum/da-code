import pandas as pd

# Read the dataset with low_memory=False to avoid DtypeWarning
df = pd.read_csv('multipleChoiceResponses.csv', low_memory=False)

# Print out the column names to find the one that contains age data
print(df.columns.tolist())
