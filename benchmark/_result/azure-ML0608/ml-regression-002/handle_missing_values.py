import pandas as pd
import numpy as np

# Load merged data
merged_data = pd.read_csv('/workspace/merged_data.csv')

# Handle missing values for numeric columns only
numeric_columns = merged_data.select_dtypes(include=[np.number]).columns
merged_data[numeric_columns] = merged_data[numeric_columns].fillna(merged_data[numeric_columns].mean())

# Save the processed data to a new CSV file
merged_data.to_csv('/workspace/processed_merged_data.csv', index=False)

# Print out a message indicating completion of missing value handling
print("Missing values handled and processed data saved.")
