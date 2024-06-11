import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the datasets
train_df = pd.read_csv('/workspace/top_10000_1960-now.csv')
test_df = pd.read_csv('/workspace/test.csv')

# Preprocessing: Select relevant numerical features and fill missing values
features = ['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Instrumentalness', 'Liveness', 'Valence', 'Tempo', 'Time Signature']
X = train_df[features]
y = train_df['Popularity']
X_test = test_df[features]

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
X = imputer.fit_transform(X)
X_test = imputer.transform(X_test)

# Scale the features
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_test = scaler.transform(X_test)

# Split the training data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred_val = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred_val)
print(f"Validation MSE: {mse}")

# Predict the popularity on the test set
test_predictions = model.predict(X_test)

# Save the predictions to a CSV file
prediction_df = pd.DataFrame(test_predictions, columns=['Popularity'])
prediction_df.to_csv('/workspace/popularity.csv', index=False)
