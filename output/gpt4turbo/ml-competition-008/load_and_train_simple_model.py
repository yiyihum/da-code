import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target
X = train_data.drop(columns=['id', 'FloodProbability'])
y = train_data['FloodProbability']

# Initialize the Linear Regression model
model = LinearRegression()

# Train the model
model.fit(X, y)

# Save the model to disk
model_filename = '/workspace/flood_prediction_model.pkl'
pd.to_pickle(model, model_filename)
