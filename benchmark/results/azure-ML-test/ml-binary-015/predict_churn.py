import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

# Load datasets
train_data = pd.read_csv('train.csv')
test_data = pd.read_csv('test.csv')

# Preprocess data
def preprocess_data(data):
    # Drop non-relevant features
    data = data.drop(columns=['id', 'CustomerId', 'Surname'])

    # Encode categorical features
    label_encoder = LabelEncoder()
    for column in ['Geography', 'Gender']:
        data[column] = label_encoder.fit_transform(data[column])

    # Fill missing values
    imputer = SimpleImputer(strategy='mean')
    data = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)

    return data

X_train = preprocess_data(train_data)
y_train = X_train.pop('Exited')

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict on test data
X_test = preprocess_data(test_data)
test_data['Exited'] = model.predict_proba(X_test)[:, 1]

# Save submission file
submission = test_data[['CustomerId', 'Exited']]
submission.to_csv('submission.csv', index=False)