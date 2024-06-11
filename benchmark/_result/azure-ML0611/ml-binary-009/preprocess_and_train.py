import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

# Load the training and test data
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Preprocessing the training data
train_data.drop(['Unnamed: 0', 'id'], axis=1, inplace=True)
test_data.drop(['Unnamed: 0', 'id'], axis=1, inplace=True)

# Handle missing values in training and test data
imputer = SimpleImputer(strategy='mean')
train_data['Arrival Delay in Minutes'] = imputer.fit_transform(train_data[['Arrival Delay in Minutes']])
test_data['Arrival Delay in Minutes'] = imputer.transform(test_data[['Arrival Delay in Minutes']])

# Encode categorical variables
label_encoder = LabelEncoder()
categorical_cols = ['Gender', 'Customer Type', 'Type of Travel', 'Class']
for col in categorical_cols:
    train_data[col] = label_encoder.fit_transform(train_data[col])
    test_data[col] = label_encoder.transform(test_data[col])

# Split training data into features and target
X_train = train_data.drop('satisfaction', axis=1)
y_train = label_encoder.fit_transform(train_data['satisfaction'])

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test data
test_data['satisfaction'] = label_encoder.inverse_transform(model.predict(test_data))

# Save the prediction results to result.csv
test_data[['satisfaction']].to_csv('/workspace/result.csv', index=False)
print("Prediction results saved to result.csv")
