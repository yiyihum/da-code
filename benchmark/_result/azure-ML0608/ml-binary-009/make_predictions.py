import pandas as pd
import joblib

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Preprocess the test data
test_df['Arrival Delay in Minutes'].fillna(test_df['Arrival Delay in Minutes'].median(), inplace=True)
test_df.drop(columns=['Unnamed: 0', 'id'], inplace=True)

# Load label encoders and encode categorical variables
categorical_cols = ['Gender', 'Customer Type', 'Type of Travel', 'Class']
for col in categorical_cols:
    le = joblib.load(f'/workspace/{col}_encoder.pkl')
    test_df[col] = le.transform(test_df[col])

# Load the trained model
model = joblib.load('/workspace/satisfaction_model.pkl')

# Make predictions
predictions = model.predict(test_df)

# Save the predictions to a CSV file
result_df = pd.DataFrame(predictions, columns=['satisfaction'])
result_df['satisfaction'] = result_df['satisfaction'].apply(lambda x: 'satisfied' if x == 1 else 'neutral or dissatisfied')
result_df.to_csv('/workspace/result.csv', index=False)

print("Predictions saved to result.csv.")
