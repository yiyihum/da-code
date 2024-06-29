import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('/workspace/data.csv')

# Replace '?' with NaN
df.replace('?', np.nan, inplace=True)

# Check for missing values in each column again
print(df.isnull().sum())
