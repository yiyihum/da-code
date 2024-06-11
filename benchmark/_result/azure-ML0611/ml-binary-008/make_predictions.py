import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Load the label encoders
with open('/workspace/label_encoders.pkl', 'rb') as file:
    label_encoders = pickle.load(file)

# Preprocess the test data in the same way as the training data
test_data.fillna({
    'Gender': test_data['Gender'].mode()[0],
    'Married': test_data['Married'].mode()[0],
    'Dependents': test_data['Dependents'].mode()[0],
    'Self_Employed': test_data['Self_Employed'].mode()[0],
    'LoanAmount': test_data['LoanAmount'].median(),
    'Loan_Amount_Term': test_data['Loan_Amount_Term'].mode()[0],
    'Credit_History': test_data['Credit_History'].mode()[0]
}, inplace=True)

# Encode categorical variables using the same label encoders as for the training data
for column in ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area']:
    test_data[column] = label_encoders[column].transform(test_data[column])

# Remove the 'Loan_ID' column as it is not a feature
X_test = test_data.drop(columns=['Loan_ID'])

# Load the trained logistic regression model
with open('/workspace/logistic_regression_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Make predictions on the test data
test_data['Loan_Status'] = model.predict(X_test)

# Inverse transform the 'Loan_Status' predictions to get 'Y' or 'N'
test_data['Loan_Status'] = label_encoders['Loan_Status'].inverse_transform(test_data['Loan_Status'])

# Save the prediction results to a CSV file
result = test_data[['Loan_Status']]
result.to_csv('/workspace/result.csv', index=False)
print("Predictions saved to result.csv.")
