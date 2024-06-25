import pandas as pd

# Load the CSV files into DataFrames
df1 = pd.read_csv('/workspace/Building_Permits_1.csv')
df2 = pd.read_csv('/workspace/Building_Permits_2.csv')
df3 = pd.read_csv('/workspace/Building_Permits_3.csv')
df4 = pd.read_csv('/workspace/Building_Permits_4.csv')

# Concatenate the DataFrames into one DataFrame
df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Save the concatenated DataFrame to a CSV file for further analysis
df.to_csv('/workspace/concatenated_permits.csv', index=False)
print("Concatenated CSV saved.")
