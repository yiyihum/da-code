import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load the training and validation data
X_train = pd.read_csv('/workspace/X_train.csv')
y_train = pd.read_csv('/workspace/y_train.csv')
X_val = pd.read_csv('/workspace/X_val.csv')
y_val = pd.read_csv('/workspace/y_val.csv')

# Initialize the Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train.values.ravel())

# Predict on the validation set
y_pred = model.predict(X_val)

# Calculate the mean squared error
mse = mean_squared_error(y_val, y_pred)
print(f"Mean Squared Error on Validation Set: {mse}")

# Save the trained model
import joblib
joblib.dump(model, '/workspace/electricity_price_model.joblib')

print("Model training completed and model saved.")
