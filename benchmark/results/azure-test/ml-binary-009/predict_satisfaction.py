import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load and preprocess the training data
train_data = pd.read_csv('train.csv')
train_data.drop(columns=['Unnamed: 0', 'id'], inplace=True)

# Handle categorical variables
categorical_cols = train_data.select_dtypes(include=['object']).columns
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    train_data[col] = le.fit_transform(train_data[col])
    label_encoders[col] = le

# Separate features and target
X_train = train_data.drop('satisfaction', axis=1)
y_train = train_data['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

# Initialize and train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Load and preprocess the test data
test_data = pd.read_csv('test.csv')
test_data.drop(columns=['Unnamed: 0', 'id'], inplace=True)
for col in test_data.columns:
    if col in label_encoders:
        le = label_encoders[col]
        test_data[col] = le.transform(test_data[col].fillna(''))

# Predict 'satisfaction' on the test data
X_test = test_data
predictions = model.predict(X_test)

# Save the predictions into 'result.csv'
result_df = pd.DataFrame(predictions, columns=['satisfaction'])
result_df['satisfaction'] = result_df['satisfaction'].apply(lambda x: 'satisfied' if x == 1 else 'neutral or dissatisfaction')
result_df.to_csv('result.csv', index=False)
