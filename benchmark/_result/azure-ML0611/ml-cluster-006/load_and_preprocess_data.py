import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/patient_dataset.csv')

# Display basic information about the dataset
print(df.info())
print(df.head())
