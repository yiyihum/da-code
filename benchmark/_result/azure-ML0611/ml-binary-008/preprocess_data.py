import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_data = pd.read_csv('/workspace/train_u6lujuX_CVtuZ9i.csv')

# Fill missing values
train_data['Gender'].fillna(train_data['Gender'].mode()[0], inplace=True)
train_data['Married'].fillna(train_data['Married'].mode()[0], inplace=True)
train_data['Dependents'].fillna(train_data['Dependents'].mode()[0], inplace=True)
train_data['Self_Employed'].fillna(train_data['Self_Employed'].mode()[0], inplace=True)
train_data['LoanAmount'].fillna(train_data['LoanAmount'].median(), inplace=True)
train_data['Loan_Amount_Term'].fillna(train_data['Loan_Amount_Term'].mode()[0], inplace=True)
train_data['Credit_History'].fillna(train_data['Credit_History'].mode()[0], inplace=True)

# Encode categorical variables
label_encoders = {}
for column in ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'Property_Area', 'Loan_Status']:
    label_encoders[column] = LabelEncoder()
    train_data[column] = label_encoders[column].fit_transform(train_data[column])

# Separate features and target variable
X = train_data.drop(columns=['Loan_ID', 'Loan_Status'])
y = train_data['Loan_Status']

# Split the data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)

# Save the preprocessed data and label encoders for later use
X_train.to_csv('/workspace/X_train.csv', index=False)
y_train.to_csv('/workspace/y_train.csv', index=False)
X_valid.to_csv('/workspace/X_valid.csv', index=False)
y_valid.to_csv('/workspace/y_valid.csv', index=False)
with open('/workspace/label_encoders.pkl', 'wb') as file:
    pickle.dump(label_encoders, file)

print("Preprocessing complete. Data split into training and validation sets.")
