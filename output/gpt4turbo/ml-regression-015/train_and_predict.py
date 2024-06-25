import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the training data
data = pd.read_csv('KAG_energydata_complete.csv')

# Preprocess the data: drop the date column and the lights column as they are not predictive
data = data.drop(['date', 'lights'], axis=1)

# Split the data into features and target
X = data.drop('Appliances', axis=1)
y = data['Appliances']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred_val = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred_val)
print(f"Validation MSE: {mse}")

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocess the test data: drop the date column and the lights column
test_data = test_data.drop(['date', 'lights'], axis=1)

# Predict the appliance energy consumption
predictions = model.predict(test_data)

# Save the predictions to a CSV file
output = pd.DataFrame(predictions, columns=['Appliances'])
output.to_csv('appliance.csv', index=False)
