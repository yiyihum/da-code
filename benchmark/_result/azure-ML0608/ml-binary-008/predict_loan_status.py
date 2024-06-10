import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

# Load the data
train_data = pd.read_csv('train_u6lujuX_CVtuZ9i.csv')
test_data = pd.read_csv('test.csv')

# Preprocessing
def preprocess_data(data):
    # Fill missing numerical values with the mean
    num_imputer = SimpleImputer(strategy='mean')
    for col in ['LoanAmount', 'Loan_Amount_Term', 'Credit_History']:
        data[col] = num_imputer.fit_transform(data[[col]]).ravel()
    
    # Encode categorical variables
    label_encoders = {}
    for column in ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area', 'Dependents']:
        label_encoders[column] = LabelEncoder()
        data[column] = label_encoders[column].fit_transform(data[column].astype(str))
    
    return data

# Preprocess the training and test data
train_data_processed = preprocess_data(train_data)
test_data_processed = preprocess_data(test_data)

# Split training data into features and target
X_train = train_data_processed.drop(columns=['Loan_ID', 'Loan_Status'])
y_train = train_data_processed['Loan_Status']

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on test data
X_test = test_data_processed.drop(columns=['Loan_ID'])
predictions = model.predict(X_test)

# Save predictions to CSV
result = pd.DataFrame({'Loan_ID': test_data['Loan_ID'], 'Loan_Status': predictions})
result.to_csv('result.csv', index=False)
