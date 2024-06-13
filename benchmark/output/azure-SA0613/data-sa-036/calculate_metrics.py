import pandas as pd

# Load the stock returns data
df = pd.read_csv('Big9Returns2017.csv')

# Initialize a dictionary to hold the results
results = {'Skewness': [], 'Fourth Moment': []}

# Calculate skewness and fourth moment (kurtosis) for each stock
for column in df.columns[1:]:  # Exclude the 'Date' column
    # Calculate skewness
    skewness = df[column].skew()
    # Calculate excess kurtosis
    excess_kurtosis = df[column].kurtosis()
    # Calculate the true fourth moment (kurtosis + 3 to adjust for excess)
    fourth_moment = excess_kurtosis + 3
    
    # Append the results
    results['Skewness'].append(skewness)
    results['Fourth Moment'].append(fourth_moment)

# Convert the results dictionary to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to the 'result.csv' file
results_df.to_csv('result.csv', index=False)
