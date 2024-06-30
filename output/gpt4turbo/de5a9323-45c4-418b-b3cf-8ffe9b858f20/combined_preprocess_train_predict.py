import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

# Load the datasets
train_df = pd.read_csv('/workspace/train.csv')
test_df = pd.read_csv('/workspace/test.csv')

# Separate features and target variable
X = train_df.drop(['id', 'Rings'], axis=1)
y = train_df['Rings']

# Preprocessing for numerical data
numerical_cols = [cname for cname in X.columns if X[cname].dtype in ['float64', 'int64']]

# Preprocessing for categorical data
categorical_cols = [cname for cname in X.columns if X[cname].dtype == 'object']

# Preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ])

# Define the model
model = RandomForestRegressor(n_estimators=100, random_state=0)

# Bundle preprocessing and modeling code in a pipeline
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('model', model)])

# Split data into train and validation subsets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# Preprocessing of training data, fit model
clf.fit(X_train, y_train)

# Preprocessing of validation data, get predictions
preds = clf.predict(X_valid)

# Evaluate the model
score = mean_squared_error(y_valid, preds, squared=False)
print('RMSE:', score)

# Preprocessing of test data, fit model
test_X = test_df.drop(['id'], axis=1)
final_preds = clf.predict(test_X)

# Save the predictions to a CSV file
output = pd.DataFrame({'id': test_df.id,
                       'Rings': np.round(final_preds).astype(int)})
output.to_csv('/workspace/submission.csv', index=False)
print("Submission file created.")
