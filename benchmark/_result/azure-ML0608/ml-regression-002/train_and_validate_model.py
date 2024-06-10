import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import joblib

# Load processed merged data
processed_data = pd.read_csv('/workspace/processed_merged_data.csv')

# Prepare features and target variable
X = processed_data.drop('price actual', axis=1)
y = processed_data['price actual']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor with fewer estimators to reduce training time
rf = RandomForestRegressor(n_estimators=10, random_state=42)
rf.fit(X_train, y_train)

# Validate the model
y_pred = rf.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
rmse = np.sqrt(mse)
print(f'Validation RMSE: {rmse}')

# Save the trained model to a file
joblib.dump(rf, '/workspace/electricity_price_predictor.joblib')
