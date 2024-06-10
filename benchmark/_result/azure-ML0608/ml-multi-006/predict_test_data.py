import pandas as pd
import joblib

# Load the label encoders and the trained model
label_encoders = pd.read_pickle('/workspace/label_encoders.pkl')
label_encoder_target = pd.read_pickle('/workspace/label_encoder_target.pkl')
rf_classifier = joblib.load('/workspace/rf_classifier.joblib')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Define the continuous and categorical variables
continuous_vars = ['Monthly_Inhand_Salary', 'Num_Credit_Inquiries', 'Amount_invested_monthly', 'Monthly_Balance', 'Changed_Credit_Limit', 'Outstanding_Debt', 'Annual_Income']
categorical_vars = ['Month', 'Occupation', 'Credit_Mix', 'Payment_of_Min_Amount', 'Payment_Behaviour']

# Preprocess the test data with the same steps as the training data
test_data['Age'] = test_data['Age'].str.extract('(\d+)').astype(float)
test_data['Annual_Income'] = pd.to_numeric(test_data['Annual_Income'].str.replace('[^0-9.]', ''), errors='coerce')
test_data['Num_of_Loan'] = test_data['Type_of_Loan'].str.count(',') + 1
test_data['Num_of_Loan'].fillna(0, inplace=True)
test_data['Changed_Credit_Limit'] = pd.to_numeric(test_data['Changed_Credit_Limit'].str.replace('_', ''), errors='coerce')
test_data['Outstanding_Debt'] = pd.to_numeric(test_data['Outstanding_Debt'].str.replace('_', ''), errors='coerce')
credit_history_extracted = test_data['Credit_History_Age'].str.extract('(\d+) Years and (\d+) Months')
test_data['Credit_History_Age'] = credit_history_extracted.apply(lambda x: int(x[0]) * 12 + int(x[1]) if pd.notnull(x[0]) and pd.notnull(x[1]) else None, axis=1)
test_data['Amount_invested_monthly'] = pd.to_numeric(test_data['Amount_invested_monthly'].str.replace('_', ''), errors='coerce')
test_data['Monthly_Balance'] = pd.to_numeric(test_data['Monthly_Balance'].str.replace('_', ''), errors='coerce')
test_data[continuous_vars] = test_data[continuous_vars].fillna(test_data[continuous_vars].mean())

# Encode categorical variables
for var in categorical_vars:
    test_data[var] = label_encoders[var].transform(test_data[var])

# Prepare the test data for prediction
X_test = test_data.drop(['ID', 'Customer_ID', 'Name', 'SSN', 'Type_of_Loan', 'Num_of_Delayed_Payment'], axis=1)

# Predict the credit scores
test_predictions = rf_classifier.predict(X_test)

# Decode the predicted credit scores back to original labels
test_predictions_decoded = label_encoder_target.inverse_transform(test_predictions)

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(test_predictions_decoded, columns=['Credit_Score'])
predictions_df.to_csv('/workspace/score.csv', index=False)

print("Predictions saved to score.csv.")
