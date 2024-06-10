import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Separate the target variable and features in the training data
X_train = train_data.drop(['id', 'Age'], axis=1)
y_train = train_data['Age']
X_test = test_data.drop(['id'], axis=1)

# Define the preprocessing for numerical and categorical features
numerical_cols = X_train.select_dtypes(include=['float64', 'int64']).columns
categorical_cols = ['Sex']

# Create the preprocessing pipelines for both numerical and categorical data
numerical_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Create the model
model = RandomForestRegressor(n_estimators=100, random_state=0)

# Create the pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])

# Split the training data for validation
X_train_full, X_valid_full, y_train_full, y_valid_full = train_test_split(X_train, y_train, train_size=0.8, test_size=0.2, random_state=0)

# Preprocessing of training data, fit model
pipeline.fit(X_train_full, y_train_full)

# Preprocessing of validation data, get predictions
preds_valid = pipeline.predict(X_valid_full)

# Evaluate the model
score = mean_squared_error(y_valid_full, preds_valid, squared=False)
print(f'RMSE: {score}')

# Preprocessing of test data, get predictions
preds_test = pipeline.predict(X_test)

# Save test predictions to file
output = pd.DataFrame({'id': test_data.id,
                       'Age': preds_test})
output.to_csv('/workspace/submission.csv', index=False)
print("Submission file created.")
