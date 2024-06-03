import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# Load the datasets
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
syn_crab_data = pd.read_csv('syn_crab_data.csv')

# Combine the 'Sex' columns of the train and syn_crab_data datasets
combined_sex = pd.concat([train['Sex'], syn_crab_data['Sex']])

# One-hot encode the combined 'Sex' column
encoder = OneHotEncoder()
encoder.fit(combined_sex.values.reshape(-1, 1))

# Save the encoder to a file
joblib.dump(encoder, 'encoder.joblib')

# Transform the 'Sex' columns of the datasets
train_encoded = pd.DataFrame(encoder.transform(train[['Sex']]).toarray())
test_encoded = pd.DataFrame(encoder.transform(test[['Sex']]).toarray())
syn_crab_data_encoded = pd.DataFrame(encoder.transform(syn_crab_data[['Sex']]).toarray())

# Replace the 'Sex' column with the encoded data
train = train.drop('Sex', axis=1)
test = test.drop('Sex', axis=1)
syn_crab_data = syn_crab_data.drop('Sex', axis=1)
train = pd.concat([train, train_encoded], axis=1)
test = pd.concat([test, test_encoded], axis=1)
syn_crab_data = pd.concat([syn_crab_data, syn_crab_data_encoded], axis=1)

# Convert all feature names to strings
train.columns = train.columns.astype(str)
test.columns = test.columns.astype(str)
syn_crab_data.columns = syn_crab_data.columns.astype(str)

# Split the training data into training and validation sets
X = train.drop('Age', axis=1)
y = train['Age']
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=0)

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=0)
model.fit(X_train, y_train)

# Save the trained model to a file
joblib.dump(model, 'model.joblib')

# Evaluate the model
predictions = model.predict(X_valid)
mae = mean_absolute_error(y_valid, predictions)
print(f'Mean Absolute Error: {mae}')
