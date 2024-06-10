import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the training and test data
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Combine train and test data to ensure consistent feature encoding
combined_data = pd.concat([train_data.drop(['id', 'Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults'], axis=1),
                           test_data.drop(['Id'], axis=1)])

# Identify numerical and categorical columns
numerical_columns = combined_data.select_dtypes(include=['int64', 'float64']).columns
categorical_columns = combined_data.select_dtypes(include=['object']).columns

# Handle missing values
# For numerical columns, fill missing values with the median
num_imputer = SimpleImputer(strategy='median')
combined_data[numerical_columns] = num_imputer.fit_transform(combined_data[numerical_columns])

# For categorical columns, fill missing values with the most frequent value
cat_imputer = SimpleImputer(strategy='most_frequent')
combined_data[categorical_columns] = cat_imputer.fit_transform(combined_data[categorical_columns])

# Convert categorical variables to dummy variables
combined_data_encoded = pd.get_dummies(combined_data)

# Split the combined data back into train and test sets
X_train_encoded = combined_data_encoded[:train_data.shape[0]]
X_test_encoded = combined_data_encoded[train_data.shape[0]:]

# Normalize the features using only the training data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_encoded)
X_test_scaled = scaler.transform(X_test_encoded)

# Separate target variables from the training data
y_train = train_data[['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']]

# Initialize the list to store predictions
predictions = []

# Train a Random Forest Classifier and make predictions for each target variable
for column in y_train.columns:
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train_scaled, y_train[column])
    
    # Make predictions
    y_test_pred_proba = clf.predict_proba(X_test_scaled)[:, 1]  # Get the probability for class 1
    predictions.append(y_test_pred_proba)

# Create the submission DataFrame
submission = pd.DataFrame(predictions).transpose()
submission.columns = y_train.columns
submission.insert(0, 'Id', test_data['Id'])

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)
