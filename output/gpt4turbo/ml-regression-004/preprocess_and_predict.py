import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Load the datasets
train_df = pd.read_csv('top_10000_1960-now.csv')
test_df = pd.read_csv('test.csv')

# Selecting relevant numerical features for modeling
features = ['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo', 'Time Signature']
X = train_df[features]
y = train_df['Popularity']

# Preprocessing: Scaling the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
test_df_scaled = scaler.transform(test_df[features])

# Split the training data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train a RandomForestRegressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_val_pred = model.predict(X_val)
val_mse = mean_squared_error(y_val, y_val_pred)
print(f'Validation MSE: {val_mse}')

# Predict the popularity on the test set
test_popularity_pred = model.predict(test_df_scaled)

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(test_popularity_pred, columns=['Popularity'])
predictions_df.to_csv('popularity.csv', index=False)
print('Predictions saved to popularity.csv')
