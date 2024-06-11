import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Preprocess the training data using the same steps as for the test data
# Impute missing values for numerical columns with median
num_cols_train = train_data.select_dtypes(include=['float64']).columns
num_imputer = SimpleImputer(strategy='median')
train_data[num_cols_train] = num_imputer.fit_transform(train_data[num_cols_train])

# Impute missing values for categorical columns with mode
cat_cols_train = train_data.select_dtypes(include=['object']).columns.drop(['PassengerId', 'Name', 'Cabin'])  # Exclude 'PassengerId', 'Name', and 'Cabin'
cat_imputer = SimpleImputer(strategy='most_frequent')
train_data[cat_cols_train] = cat_imputer.fit_transform(train_data[cat_cols_train])

# Convert boolean columns to binary
bool_cols_train = ['CryoSleep', 'VIP', 'Transported']
train_data[bool_cols_train] = train_data[bool_cols_train].astype(bool)

# One-hot encode categorical variables
encoder = OneHotEncoder(drop='first')
encoded_cats_train = encoder.fit_transform(train_data[cat_cols_train]).toarray()
encoded_cats_train_df = pd.DataFrame(encoded_cats_train, columns=encoder.get_feature_names_out(cat_cols_train))

# Drop the original categorical columns and concatenate the new one-hot encoded columns
train_data = train_data.drop(columns=cat_cols_train)
train_data = pd.concat([train_data, encoded_cats_train_df], axis=1)

# Drop 'Name', 'Cabin', and 'PassengerId' columns as they are not needed for the model
train_data = train_data.drop(columns=['Name', 'Cabin', 'PassengerId'])

# Split the training data into features and target variable
X_train = train_data.drop('Transported', axis=1)
y_train = train_data['Transported']

# Train a Random Forest Classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Load the preprocessed test data
test_data = pd.read_csv('/workspace/preprocessed_test_data.csv')

# Ensure the test data has the same features as the training data
test_data = test_data.drop(columns=['PassengerId'])

# Predict on the test data
predictions = clf.predict(test_data)

# Load the original test data to merge 'PassengerId' with predictions
original_test_data = pd.read_csv('/workspace/test.csv')

# Create a submission DataFrame
submission = pd.DataFrame({
    'PassengerId': original_test_data['PassengerId'],
    'Transported': predictions
})

# Save the submission file
submission_file_path = '/workspace/submission.csv'
submission.to_csv(submission_file_path, index=False)

print("Model trained and predictions saved to:", submission_file_path)
