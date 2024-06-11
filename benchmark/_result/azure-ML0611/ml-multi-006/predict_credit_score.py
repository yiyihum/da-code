import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import re
import numpy as np

# Function to clean non-numeric characters from numeric columns
def clean_numeric_columns(df, columns):
    for col in columns:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace('[^0-9.]', ''), errors='coerce')
    return df

# Function to convert credit history age to months
def convert_credit_history_age_to_months(df, column):
    def age_to_months(age_str):
        if pd.isnull(age_str):
            return None
        years_months = re.findall(r'(\d+)\sYears\sand\s(\d+)\sMonths', age_str)
        if years_months:
            years, months = years_months[0]
            return int(years) * 12 + int(months)
        return None
    df[column] = df[column].apply(age_to_months)
    return df

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Preprocessing
# Clean non-numeric characters
numeric_columns = ['Age', 'Annual_Income', 'Monthly_Inhand_Salary', 'Num_Bank_Accounts', 'Num_Credit_Card', 'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment', 'Changed_Credit_Limit', 'Num_Credit_Inquiries', 'Outstanding_Debt', 'Credit_Utilization_Ratio', 'Total_EMI_per_month', 'Amount_invested_monthly', 'Monthly_Balance']
train_data = clean_numeric_columns(train_data, numeric_columns)

# Convert 'Credit_History_Age' to numeric
train_data = convert_credit_history_age_to_months(train_data, 'Credit_History_Age')

# Fill missing values
train_data.ffill(inplace=True)

# Drop columns that are not needed for modeling to simplify the model
columns_to_drop = ['Customer_ID', 'Month', 'Name', 'SSN', 'Occupation', 'Type_of_Loan', 'Credit_Mix', 'Payment_of_Min_Amount', 'Payment_Behaviour']
train_data.drop(columns=columns_to_drop, inplace=True)

# Split the data into features and target
X = train_data.drop(columns=['ID', 'Credit_Score'])
y = train_data['Credit_Score']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model with a minimal number of estimators to speed up the process
model = RandomForestClassifier(random_state=42, n_estimators=5)
model.fit(X_train, y_train)

# Validate the model
y_pred = model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print(f'Validation Accuracy: {accuracy}')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data using the same steps as for the training data
test_data = clean_numeric_columns(test_data, numeric_columns)
test_data = convert_credit_history_age_to_months(test_data, 'Credit_History_Age')
test_data.ffill(inplace=True)
test_data.drop(columns=columns_to_drop, inplace=True)

# Predict the credit scores
X_test = test_data.drop(columns=['ID'])
predictions = model.predict(X_test)

# Save the predictions to a CSV file
output = pd.DataFrame({'ID': test_data['ID'], 'Credit_Score': predictions})
output.to_csv('/workspace/score.csv', index=False)
