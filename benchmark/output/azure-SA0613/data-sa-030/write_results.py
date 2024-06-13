import pandas as pd

# Load the existing result.csv file
result_df = pd.read_csv('/workspace/result.csv')

# Assuming the result.csv has the correct format with headers for periods
# and we just need to fill in the calculated VaR values.
# If the file is empty or has a different structure, this code will need to be adjusted.
result_df.loc[0, '2005-2006'] = 0.014687184472834543
result_df.loc[0, '2007-2009'] = 0.0579057406681419

# Save the updated results back to result.csv
result_df.to_csv('/workspace/result.csv', index=False)
