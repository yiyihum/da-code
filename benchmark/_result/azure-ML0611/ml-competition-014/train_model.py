import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Preprocess the data: Here we'll just use the 'active' feature for simplicity
X = train_data[['active']]
y = train_data['microbusiness_density']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
mape = mean_absolute_percentage_error(y_val, y_pred)
print(f"Validation MAPE: {mape}")

# Save the trained model to a file
model_filename = '/workspace/microbusiness_model.pkl'
pd.to_pickle(model, model_filename)
print(f"Model saved to {model_filename}")
