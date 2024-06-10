import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Preprocessing steps:

# Convert 'Age' to numeric by removing non-numeric characters and converting to integer
train_data['Age'] = train_data['Age'].str.extract('(\d+)').astype(float)

# Convert 'Annual_Income' to numeric by removing non-numeric characters and converting to float
train_data['Annual_Income'] = pd.to_numeric(train_data['Annual_Income'].str.replace('[^0-9.]', ''), errors='coerce')

# Convert 'Num_of_Loan' to numeric by counting the number of loans listed
train_data['Num_of_Loan'] = train_data['Type_of_Loan'].str.count(',') + 1
train_data['Num_of_Loan'].fillna(0, inplace=False)  # Assuming empty means no loans

# Handle 'Changed_Credit_Limit' by removing non-numeric characters and converting to float
train_data['Changed_Credit_Limit'] = pd.to_numeric(train_data['Changed_Credit_Limit'].str.replace('_', ''), errors='coerce')

# Handle 'Outstanding_Debt' by removing non-numeric characters and converting to float
train_data['Outstanding_Debt'] = pd.to_numeric(train_data['Outstanding_Debt'].str.replace('_', ''), errors='coerce')

# Convert 'Credit_History_Age' to numeric by extracting the number of months
credit_history_extracted = train_data['Credit_History_Age'].str.extract('(\d+) Years and (\d+) Months')
train_data['Credit_History_Age'] = credit_history_extracted.apply(lambda x: int(x[0]) * 12 + int(x[1]) if pd.notnull(x[0]) and pd.notnull(x[1]) else None, axis=1)

# Handle 'Amount_invested_monthly' by removing non-numeric characters and converting to float
train_data['Amount_invested_monthly'] = pd.to_numeric(train_data['Amount_invested_monthly'].str.replace('_', ''), errors='coerce')

# Handle 'Monthly_Balance' by removing non-numeric characters and converting to float
train_data['Monthly_Balance'] = pd.to_numeric(train_data['Monthly_Balance'].str.replace('_', ''), errors='coerce')

# Fill missing values with mean for continuous variables
continuous_vars = ['Monthly_Inhand_Salary', 'Num_Credit_Inquiries', 'Amount_invested_monthly', 'Monthly_Balance', 'Changed_Credit_Limit', 'Outstanding_Debt', 'Annual_Income']
train_data[continuous_vars] = train_data[continuous_vars].fillna(train_data[continuous_vars].mean())

# Encode categorical variables including 'Month' which was previously overlooked
categorical_vars = ['Month', 'Occupation', 'Credit_Mix', 'Payment_of_Min_Amount', 'Payment_Behaviour']
label_encoders = {}
for var in categorical_vars:
    label_encoders[var] = LabelEncoder()
    train_data[var] = label_encoders[var].fit_transform(train_data[var])

# Encode target variable
label_encoder_target = LabelEncoder()
train_data['Credit_Score'] = label_encoder_target.fit_transform(train_data['Credit_Score'])

# Split the data into training and validation sets
X = train_data.drop(['ID', 'Customer_ID', 'Name', 'SSN', 'Type_of_Loan', 'Num_of_Delayed_Payment', 'Credit_Score'], axis=1)
y = train_data['Credit_Score']
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Save the preprocessed data and label encoders for later use
X_train.to_csv('/workspace/X_train.csv', index=False)
y_train.to_csv('/workspace/y_train.csv', index=False)
X_val.to_csv('/workspace/X_val.csv', index=False)
y_val.to_csv('/workspace/y_val.csv', index=False)
pd.to_pickle(label_encoders, '/workspace/label_encoders.pkl')
pd.to_pickle(label_encoder_target, '/workspace/label_encoder_target.pkl')

print("Preprocessing complete. Data split into training and validation sets.")
