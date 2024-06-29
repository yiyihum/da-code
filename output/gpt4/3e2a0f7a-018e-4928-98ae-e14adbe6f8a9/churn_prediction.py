import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load the data
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Store the 'CustomerId' from the test data for the submission file
test_ids = test_data['CustomerId']

# Preprocess the data
def preprocess_data(data):
    # Drop the 'Surname' and 'CustomerId' columns as they are not useful for prediction
    data = data.drop(columns=['Surname', 'CustomerId'])
    
    # Convert categorical variables to numeric using label encoding
    label_encoder = LabelEncoder()
    categorical_columns = ['Geography', 'Gender']
    for col in categorical_columns:
        data[col] = label_encoder.fit_transform(data[col])
    
    # Fill missing values with the median
    data = data.fillna(data.median())
    
    return data

train_data = preprocess_data(train_data)
test_data = preprocess_data(test_data)

# Separate features and target variable
X = train_data.drop(columns=['Exited', 'id'])
y = train_data['Exited']

# Split the training data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_pred_val = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred_val)
print(f'Validation accuracy: {accuracy}')

# Make predictions on the test data
X_test = test_data
test_predictions = model.predict_proba(X_test)[:, 1]

# Create the submission file
submission = pd.DataFrame({'id': test_ids, 'Exited': test_predictions})
submission.to_csv('/workspace/submission.csv', index=False)
