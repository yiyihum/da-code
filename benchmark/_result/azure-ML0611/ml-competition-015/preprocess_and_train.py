from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import median_absolute_error
import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target variable
X = train_data.drop(columns=['id', 'Hardness'])
y = train_data['Hardness']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
rf_regressor.fit(X_train, y_train)

# Predict on the validation set
y_pred = rf_regressor.predict(X_val)

# Calculate the Median Absolute Error
medae = median_absolute_error(y_val, y_pred)
print(f'Median Absolute Error on the validation set: {medae}')
