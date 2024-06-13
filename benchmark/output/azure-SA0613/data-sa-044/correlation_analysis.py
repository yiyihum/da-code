import pandas as pd

# Load the dataset
df = pd.read_csv('car_insurance.csv')

# Drop the 'id' column as it is not needed for correlation analysis
df = df.drop(columns=['id'])

# Convert non-numeric columns to numeric where possible and drop those that cannot be converted
for column in df.columns:
    # Try to convert the column to numeric, if not possible, drop the column
    try:
        df[column] = pd.to_numeric(df[column])
    except ValueError:
        df = df.drop(columns=[column])

# Calculate the correlation matrix
correlation_matrix = df.corr()

# Find the variable with the highest correlation with 'outcome'
outcome_correlation = correlation_matrix['outcome'].drop(labels=['outcome'])
max_correlation_variable = outcome_correlation.idxmax()

# Write the result to the result.csv file
result_df = pd.DataFrame({'variable': [max_correlation_variable]})
result_df.to_csv('result.csv', index=False)
