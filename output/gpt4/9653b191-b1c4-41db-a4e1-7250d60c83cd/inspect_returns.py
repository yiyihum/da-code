import pandas as pd

# Load the stock return data and set 'Date' as the index
returns = pd.read_csv('Big9Returns2017.csv', index_col='Date', parse_dates=True)

# Print the columns of the 'returns' DataFrame to identify the extra column
print("Columns in returns DataFrame:", returns.columns)
