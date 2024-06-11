import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target
X = train_data.drop(columns=['id', 'FloodProbability'])
y = train_data['FloodProbability']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the XGBoost regressor
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)

# Fit the model to the training data
model.fit(X_train, y_train)

# Predict on the validation set
y_pred = model.predict(X_val)

# Calculate the root mean squared error (RMSE) on the validation set
rmse = mean_squared_error(y_val, y_pred, squared=False)
print(f'Validation RMSE: {rmse}')
