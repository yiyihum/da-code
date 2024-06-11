import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

# Load the preprocessed training data
X_train = pd.read_csv('/workspace/X_train.csv')
y_train = pd.read_csv('/workspace/y_train.csv')
X_val = pd.read_csv('/workspace/X_val.csv')
y_val = pd.read_csv('/workspace/y_val.csv')

# Initialize the RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train.values.ravel())

# Make predictions on the validation set
y_pred = model.predict(X_val)

# Calculate the r2 score
r2 = r2_score(y_val, y_pred)

# Output the r2 score
print(f"Validation r2 score: {r2}")

# Save the trained model for later use
import joblib
joblib.dump(model, '/workspace/delivery_time_predictor.joblib')
