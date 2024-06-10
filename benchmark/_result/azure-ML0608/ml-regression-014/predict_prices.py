import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Load the training and test data
train_data = pd.read_csv('Car_Prices_Poland_Kaggle.csv')
test_data = pd.read_csv('test.csv')

# Combine the data to fit the label encoders
combined_data = pd.concat([train_data, test_data], sort=False)

# Preprocess the data
# Encode categorical variables
label_encoders = {}
for column in ['mark', 'model', 'generation_name', 'fuel', 'city', 'province']:
    label_encoders[column] = LabelEncoder()
    combined_data[column] = label_encoders[column].fit_transform(combined_data[column].astype(str))

# Separate the training and test data again
train_data = combined_data[:len(train_data)].copy()
test_data = combined_data[len(train_data):].copy()

# Split features and target for training data
X_train = train_data.drop(columns=['Unnamed: 0', 'price'])
y_train = train_data['price']

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Prepare test data for prediction
X_test = test_data.drop(columns=['Unnamed: 0', 'price'])

# Predict prices
X_test['price'] = model.predict(X_test)

# Save the predictions to a new file
X_test[['price']].to_csv('price.csv', index=False)
