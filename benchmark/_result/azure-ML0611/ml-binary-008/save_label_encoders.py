import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_data = pd.read_csv('/workspace/train_u6lujuX_CVtuZ9i.csv')

# Fill missing values
train_data.fillna({
    'Gender': train_data['Gender'].mode()[0],
    'Married': train_data['Married'].mode()[0],
    'Dependents': train_data['Dependents'].mode()[0],
    'Self_Employed': train_data['Self_Employed'].mode()[0],
    'LoanAmount': train_data['LoanAmount'].median(),
    'Loan_Amount_Term': train_data['Loan_Amount_Term'].mode()[0],
    'Credit_History': train_data['Credit_History'].mode()[0]
}, inplace=True)

# Encode categorical variables
label_encoders = {}
for column in ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area', 'Loan_Status']:
    label_encoders[column] = LabelEncoder()
    train_data[column] = label_encoders[column].fit_transform(train_data[column])

# Save the label encoders for later use
with open('/workspace/label_encoders.pkl', 'wb') as file:
    pickle.dump(label_encoders, file)

print("Label encoders saved.")
