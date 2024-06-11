import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Separate features and target variable
X = train_data.drop(['id', 'Age'], axis=1)
y = train_data['Age']
X_test = test_data.drop(['id'], axis=1)

# Preprocessing for numerical data
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns
numerical_transformer = StandardScaler()

# Preprocessing for categorical data
categorical_features = ['Sex']
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Define the model
model = RandomForestRegressor(n_estimators=100, random_state=0)

# Bundle preprocessing and modeling code in a pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])

# Split data into train and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# Preprocessing of training data, fit model
pipeline.fit(X_train, y_train)

# Preprocessing of validation data, get predictions
preds = pipeline.predict(X_valid)

# Evaluate the model
score = mean_squared_error(y_valid, preds, squared=False)
print(f'RMSE: {score}')

# Preprocessing of test data, fit model
preds_test = pipeline.predict(X_test)

# Save test predictions to file
output = pd.DataFrame({'id': test_data.id,
                       'Age': preds_test})
output.to_csv('/workspace/submission.csv', index=False)
print('Test predictions saved to submission.csv')
