import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import log_loss

# Load the training and test data
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Separate features and target variable
X = train_data.drop(['id', 'Status'], axis=1)
y = train_data['Status']
status_mapping = {'C': 0, 'CL': 1, 'D': 2}
y_encoded = y.map(status_mapping)

# Identify categorical and numerical columns
categorical_cols = X.select_dtypes(include=['object']).columns
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns

# Create the preprocessing pipelines for both numeric and categorical data
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Create the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Create the pipeline
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', model)])

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train the model
clf.fit(X_train, y_train)

# Predict probabilities on the test set
test_pred = clf.predict_proba(test_data.drop(['id'], axis=1))

# Create a DataFrame with the predictions
submission = pd.DataFrame(test_pred, columns=['Status_C', 'Status_CL', 'Status_D'])

# Add the 'id' column from the test data
submission.insert(0, 'id', test_data['id'])

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)

# Display the first few lines of the submission file
print(submission.head())
