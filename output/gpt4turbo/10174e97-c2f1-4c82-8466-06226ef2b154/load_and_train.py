import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target
X = train_data.drop(columns=['id', 'FloodProbability'])
y = train_data['FloodProbability']

# Initialize the model with fewer estimators to speed up training
model = RandomForestRegressor(n_estimators=10, random_state=42)

# Train the model
model.fit(X, y)

# Save the model to disk
model_filename = '/workspace/flood_prediction_model.pkl'
pd.to_pickle(model, model_filename)
