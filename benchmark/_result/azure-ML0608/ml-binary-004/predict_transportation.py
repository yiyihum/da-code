import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocessing
# Impute missing numerical data with median
numerical_transformer = SimpleImputer(strategy='median')

# Impute missing categorical data with the most frequent value and encode
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Columns that will be used in the model
numerical_cols = test_data.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = test_data.select_dtypes(include=['object', 'bool']).columns

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Define the model
model = RandomForestClassifier(n_estimators=100, random_state=0)

# Create and evaluate the pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])

# We don't have the true labels for the test set, so we can't evaluate the model.
# Instead, we'll fit the model on the entire training data and make predictions on the test set.
# Load the training data
train_data = pd.read_csv('/workspace/train.csv')
X_train = train_data.drop(['Transported'], axis=1)
y_train = train_data['Transported']

# Preprocessing of training data, fit model
pipeline.fit(X_train, y_train)

# Preprocessing of test data, get predictions
predictions = pipeline.predict(test_data)

# Save the predictions to a CSV file
output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Transported': predictions})
output.to_csv('/workspace/submission.csv', index=False)
