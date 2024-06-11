import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

# Load the cleaned training and test data
train_data = pd.read_csv('/workspace/clean_train.csv')
test_data = pd.read_csv('/workspace/clean_test.csv')

# Separate features and target variable from the training data
X_train = train_data.drop('NObeyesdad', axis=1)
y_train = train_data['NObeyesdad']
X_test = test_data.drop('id', axis=1)
test_ids = test_data['id']

# List of categorical columns to be one-hot encoded
categorical_cols = [cname for cname in X_train.columns if X_train[cname].dtype == "object"]

# List of numerical columns
numerical_cols = [cname for cname in X_train.columns if X_train[cname].dtype in ['int64', 'float64']]

# Preprocessing for numerical data
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)])

# Preprocess the training and test data
X_train = preprocessor.fit_transform(X_train)
X_test = preprocessor.transform(X_test)

# Initialize and train the model
model = RandomForestClassifier(n_estimators=100, random_state=0)
model.fit(X_train, y_train)

# Make predictions on the test set
test_preds = model.predict(X_test)

# Create the submission file
submission = pd.DataFrame({'id': test_ids, 'NObeyesdad': test_preds})
submission.to_csv('/workspace/submission.csv', index=False)

print("Submission file created successfully.")
