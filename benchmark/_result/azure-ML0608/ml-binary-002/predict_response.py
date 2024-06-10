import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Combine train and test data to ensure label encoding covers all categories
combined_data = pd.concat([train_data, test_data], axis=0)

# Preprocessing
# Convert categorical variables to numerical
label_encoder = LabelEncoder()
categorical_cols = ['Gender', 'Vehicle_Age', 'Vehicle_Damage']
for col in categorical_cols:
    combined_data[col] = label_encoder.fit_transform(combined_data[col])

# Split the combined data back into train and test sets
train_data = combined_data.iloc[:train_data.shape[0], :]
test_data = combined_data.iloc[train_data.shape[0]:, :]

# Split the training data into features and target variable
X = train_data.drop(['id', 'Response'], axis=1)
y = train_data['Response']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print(f'Validation Accuracy: {accuracy}')

# Make predictions on the test data
test_data['Response'] = model.predict(test_data.drop(['id', 'Response'], axis=1))

# Create the submission file
submission = test_data[['id', 'Response']]
submission.to_csv('/workspace/submission.csv', index=False)
