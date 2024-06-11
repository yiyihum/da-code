import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load the training data
train_data = pd.read_csv('/workspace/drugsComTrain_raw.csv')

# Preprocess the training data
train_data = train_data.drop(['Unnamed: 0', 'date'], axis=1)
train_data['condition'].fillna('Unknown', inplace=True)

# Select features and target variable for the model
X_train = train_data[['rating']]
y_train = train_data['usefulCount']

# Initialize and train the random forest regressor
regressor = RandomForestRegressor(n_estimators=100, random_state=42)
regressor.fit(X_train, y_train)

# Load the test data from the correct file
test_data = pd.read_csv('/workspace/drugLibTest_raw.csv')

# Predict the 'usefulCount' (usefulness) on the test data
test_data['usefulness'] = regressor.predict(test_data[['rating']])

# Create the 'Usefulness.csv' file with only the 'usefulness' column
test_data[['usefulness']].to_csv('/workspace/Usefulness.csv', index=False)
