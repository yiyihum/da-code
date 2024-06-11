import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# Load the training data
train_df = pd.read_csv('/workspace/train.csv')

# Split the training data into features and target
X = train_df.drop(['id', 'yield'], axis=1)
y = train_df['yield']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize a Random Forest Regressor as a baseline model
rf = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
rf.fit(X_train, y_train)

# Make predictions on the validation set
y_pred = rf.predict(X_val)

# Calculate the mean absolute error (MAE) on the validation set
mae_val = mean_absolute_error(y_val, y_pred)
print(f"Validation MAE: {mae_val}")
