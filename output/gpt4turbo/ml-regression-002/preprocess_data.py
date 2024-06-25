import pandas as pd
from sklearn.model_selection import train_test_split

# Load the datasets
energy_data = pd.read_csv('/workspace/energy_dataset.csv')

# Drop columns with a large number of missing values
columns_to_drop = ['generation hydro pumped storage aggregated', 'forecast wind offshore eday ahead']
energy_data = energy_data.drop(columns=columns_to_drop)

# Impute missing values with the mean of the column
for column in energy_data.columns:
    if energy_data[column].isnull().any():
        energy_data[column].fillna(energy_data[column].mean(), inplace=True)

# Confirm that there are no more missing values
print("Missing Values After Imputation:")
print(energy_data.isnull().sum())

# Prepare features and target variable
X = energy_data.drop(columns=['time', 'price actual'])
y = energy_data['price actual']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Save the processed data
X_train.to_csv('/workspace/X_train.csv', index=False)
y_train.to_csv('/workspace/y_train.csv', index=False)
X_val.to_csv('/workspace/X_val.csv', index=False)
y_val.to_csv('/workspace/y_val.csv', index=False)

print("Data preprocessing completed and files saved.")
