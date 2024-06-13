import pandas as pd

# Define the z-statistic and p-value obtained from the z-test
z_statistic = 2.3854622238608965
p_value = 0.00852883707474276

# Create a DataFrame with the results
results_df = pd.DataFrame({
    'Z-statistic': [z_statistic],
    'p-value': [p_value]
})

# Write the results to the result.csv file
results_df.to_csv('/workspace/result.csv', index=False)
