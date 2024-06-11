import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Separate features and target variable
X = train_data.drop(['id', 'Rings'], axis=1)
y = train_data['Rings']

# Preprocessing for numerical data
numerical_cols = [cname for cname in X.columns if X[cname].dtype in ['float64', 'int64']]
numerical_transformer = StandardScaler()

# Preprocessing for categorical data
categorical_cols = [cname for cname in X.columns if X[cname].dtype == "object"]
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Define the model
model = LinearRegression()

# Bundle preprocessing and modeling code in a pipeline
my_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('model', model)])

# Split data into train and validation subsets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# Preprocessing of training data, fit model
my_pipeline.fit(X_train, y_train)

# Preprocessing of validation data, get predictions
preds = my_pipeline.predict(X_valid)

# Evaluate the model
score = mean_squared_error(y_valid, preds, squared=False)
print('RMSE:', score)

# Preprocessing of test data, fit model
test_X = test_data.drop(['id'], axis=1)
final_predictions = my_pipeline.predict(test_X)

# Save the predictions to a CSV file
output = pd.DataFrame({'id': test_data.id,
                       'Rings': final_predictions})
output.to_csv('/workspace/submission.csv', index=False)
print("Submission file saved.")
