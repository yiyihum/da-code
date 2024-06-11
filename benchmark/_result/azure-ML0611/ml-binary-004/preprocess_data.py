import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Impute missing values for numerical columns with median
num_cols = test_data.select_dtypes(include=['float64']).columns
num_imputer = SimpleImputer(strategy='median')
test_data[num_cols] = num_imputer.fit_transform(test_data[num_cols])

# Impute missing values for categorical columns with mode
cat_cols = test_data.select_dtypes(include=['object']).columns.drop(['PassengerId', 'Name', 'Cabin'])  # Exclude 'PassengerId', 'Name', and 'Cabin'
cat_imputer = SimpleImputer(strategy='most_frequent')
test_data[cat_cols] = cat_imputer.fit_transform(test_data[cat_cols])

# Convert boolean columns to binary
bool_cols = ['CryoSleep', 'VIP']
test_data[bool_cols] = test_data[bool_cols].astype(bool)

# One-hot encode categorical variables
encoder = OneHotEncoder(drop='first')
encoded_cats = encoder.fit_transform(test_data[cat_cols]).toarray()
encoded_cats_df = pd.DataFrame(encoded_cats, columns=encoder.get_feature_names_out(cat_cols))

# Drop the original categorical columns and concatenate the new one-hot encoded columns
test_data = test_data.drop(columns=cat_cols)
test_data = pd.concat([test_data, encoded_cats_df], axis=1)

# Drop 'Name' and 'Cabin' columns as they are not needed for the model
test_data = test_data.drop(columns=['Name', 'Cabin'])

# Save the preprocessed data to a new CSV file for further use
preprocessed_file_path = '/workspace/preprocessed_test_data.csv'
test_data.to_csv(preprocessed_file_path, index=False)

print("Preprocessing complete. Data saved to:", preprocessed_file_path)
