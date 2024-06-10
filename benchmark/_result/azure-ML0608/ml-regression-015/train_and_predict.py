import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the complete dataset
complete_data = pd.read_csv('/workspace/KAG_energydata_complete.csv')

# Preprocess the data: drop non-numeric columns and check for missing values
complete_data = complete_data.select_dtypes(include=[np.number])
complete_data = complete_data.dropna()

# Separate the features and target variable
X = complete_data.drop('Appliances', axis=1)
y = complete_data['Appliances']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred_val = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred_val)
print(f"Validation MSE: {mse}")

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data: drop non-numeric columns and ensure it has the same features as the training set
test_data = test_data.select_dtypes(include=[np.number])
test_data = test_data[X_train.columns]

# Predict the appliance energy consumption
predictions = model.predict(test_data)

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(predictions, columns=['Appliances'])
predictions_df.to_csv('/workspace/appliance.csv', index=False)
