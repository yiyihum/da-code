import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the training data
train_df = pd.read_csv('train.csv')

# Drop the identifiers
train_df.drop(columns=['Unnamed: 0', 'id'], inplace=True)

# Encode categorical features
categorical_features = ['Gender', 'Customer Type', 'Type of Travel', 'Class']
label_encoders = {}

for feature in categorical_features:
    le = LabelEncoder()
    train_df[feature] = le.fit_transform(train_df[feature])
    label_encoders[feature] = le

# Handle missing values (if any)
train_df = train_df.fillna(0)

# Separate features and target
X_train = train_df.drop(columns=['satisfaction'])
y_train = train_df['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the model to disk
joblib.dump(model, 'model.pkl')

# Load test data
test_df = pd.read_csv('test.csv')

# Drop the identifiers
test_df.drop(columns=['Unnamed: 0', 'id'], inplace=True)

# Encode categorical features using the same encoders from the training
for feature in categorical_features:
    test_df[feature] = label_encoders[feature].transform(test_df[feature])

# Handle missing values (if any)
test_df = test_df.fillna(0)

# Make predictions
X_test = test_df
predictions = model.predict(X_test)

# Save predictions to 'result.csv' - map 1 back to 'satisfied' and 0 to 'not_satisfied'
result_df = pd.DataFrame(predictions, columns=['satisfaction'])
result_df['satisfaction'] = result_df['satisfaction'].apply(lambda x: 'satisfied' if x == 1 else 'not_satisfied')
result_df.to_csv('result.csv', index=False)