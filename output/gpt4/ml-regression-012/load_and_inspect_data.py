import pandas as pd

# Load the datasets
ny_cars_data = pd.read_csv('/workspace/New_York_cars.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Display the first few rows of each dataset
print("New York Cars Dataset:")
print(ny_cars_data.head())
print("\nTest Dataset:")
print(test_data.head())

# Display the data types and missing values
print("\nData types and missing values for New York Cars Dataset:")
print(ny_cars_data.info())
print("\nData types and missing values for Test Dataset:")
print(test_data.info())
