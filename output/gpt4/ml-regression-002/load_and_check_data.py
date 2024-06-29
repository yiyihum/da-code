import pandas as pd

# Load the datasets
energy_data = pd.read_csv('/workspace/energy_dataset.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Display the first few rows of the datasets
print("Energy Dataset Head:")
print(energy_data.head())
print("\nTest Dataset Head:")
print(test_data.head())

# Check for missing values in the datasets
print("\nMissing Values in Energy Dataset:")
print(energy_data.isnull().sum())
print("\nMissing Values in Test Dataset:")
print(test_data.isnull().sum())

# Check the data types of the columns
print("\nData Types in Energy Dataset:")
print(energy_data.dtypes)
print("\nData Types in Test Dataset:")
print(test_data.dtypes)
