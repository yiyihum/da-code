import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Load the datasets
train_data = pd.read_csv('train_u6lujuX_CVtuZ9i.csv')
test_data = pd.read_csv('test.csv')

# Preprocessing
def preprocess_data(train, test):
    # Combine train and test data to ensure consistent label encoding
    combined = pd.concat([train.drop(columns=['Loan_Status']), test])
    
    # Fill missing numerical values with mean
    num_cols = combined.select_dtypes(include=['float64', 'int64']).columns
    for col in num_cols:
        combined[col].fillna(combined[col].mean(), inplace=True)
    
    # Encode categorical variables
    cat_cols = combined.select_dtypes(include=['object']).columns
    le_dict = {}
    for col in cat_cols:
        if col != 'Loan_ID':  # Do not encode Loan_ID
            le = LabelEncoder()
            combined[col] = le.fit_transform(combined[col])
            le_dict[col] = le
    
    # Split combined back into train and test
    train_processed = combined.iloc[:train.shape[0], :]
    test_processed = combined.iloc[train.shape[0]:, :]
    
    # Add the Loan_Status column back to train_processed
    train_processed['Loan_Status'] = train['Loan_Status'].values
    
    return train_processed, test_processed

# Preprocess the datasets
train_data_processed, test_data_processed = preprocess_data(train_data, test_data)

# Separate features and target variable
X = train_data_processed.drop(columns=['Loan_ID', 'Loan_Status'])
y = train_data_processed['Loan_Status'].apply(lambda x: 1 if x == 'Y' else 0)

# Split the training data for validation
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Validate the model
y_pred_val = model.predict(X_val)
print(f"Validation Accuracy: {accuracy_score(y_val, y_pred_val)}")

# Make predictions on the test data
test_features = test_data_processed.drop(columns=['Loan_ID'])
predictions = model.predict(test_features)

# Prepare the results dataframe
results = pd.DataFrame({
    'Loan_ID': test_data['Loan_ID'],
    'Loan_Status': predictions
})

# Replace encoded labels back to original
results['Loan_Status'] = np.where(results['Loan_Status'] == 1, 'Y', 'N')

# Save the predictions to a CSV file
results.to_csv('result.csv', index=False)
