import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Load the data
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Preprocessing function to clean and prepare the data
def preprocess_data(data):
    # Handle missing values
    data = data.fillna(data.mean(numeric_only=True))
    for column in data.columns:
        if data[column].dtype == 'object':
            data[column] = data[column].fillna('Unknown')
            # Encode categorical variables
            le = LabelEncoder()
            data[column] = le.fit_transform(data[column])
    return data

# Preprocess the training and test data
train_data = preprocess_data(train_data)
test_data = preprocess_data(test_data)

# Split the training data into features and target
X_train = train_data.drop(columns=['ID', 'Time_taken(min)'])
y_train = train_data['Time_taken(min)']

# Train the model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test data
predictions = model.predict(test_data)

# Create the submission file
submission = pd.DataFrame({
    'ID': test_data.index.astype(str),
    'Time_taken (min)': predictions
})
submission['ID'] = '0x' + submission['ID'].apply(lambda x: x.zfill(4))
submission.to_csv('/workspace/submission.csv', index=False)
