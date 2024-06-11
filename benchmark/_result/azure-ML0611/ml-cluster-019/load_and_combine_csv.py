import pandas as pd

# Specify the encoding to handle special characters
encoding = 'ISO-8859-1'

# Load the CSV files into DataFrames with the specified encoding
df_2009_2010 = pd.read_csv('Year 2009-2010.csv', encoding=encoding)
df_2010_2011 = pd.read_csv('Year 2010-2011.csv', encoding=encoding)

# Combine the DataFrames into one
df_combined = pd.concat([df_2009_2010, df_2010_2011], ignore_index=True)

# Save the combined DataFrame to a new CSV for further processing
df_combined.to_csv('/workspace/combined_data.csv', index=False)

# Output the shape of the combined DataFrame
print(df_combined.shape)
