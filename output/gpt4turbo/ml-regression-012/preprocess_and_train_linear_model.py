import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the datasets
ny_cars_data = pd.read_csv('/workspace/New_York_cars.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Impute the missing values in the 'Mileage' column
ny_cars_data['Mileage'].fillna(ny_cars_data['Mileage'].mean(), inplace=True)

# Define the features and target variable
features = ny_cars_data.drop(columns=['Mileage', 'currency', 'name'])
target = ny_cars_data['Mileage']

# Preprocessing for numerical data
numerical_transformer = SimpleImputer(strategy='mean')

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, features.select_dtypes(exclude=['object']).columns),
        ('cat', categorical_transformer, features.select_dtypes(include=['object']).columns)
    ])

# Define the model as Linear Regression
model = LinearRegression()

# Bundle preprocessing and modeling code in a pipeline
my_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('model', model)])

# Split data into train and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(features, target, train_size=0.8, test_size=0.2, random_state=0)

# Preprocessing of training data, fit model
my_pipeline.fit(X_train, y_train)

# Preprocessing of validation data, get predictions
preds = my_pipeline.predict(X_valid)

# Evaluate the model
score = mean_squared_error(y_valid, preds, squared=False)
print('RMSE:', score)

# Preprocessing of test data, fit model
preds_test = my_pipeline.predict(test_data.drop(columns=['currency', 'name']))

# Save the predictions to a CSV file
output = pd.DataFrame({'Mileage': preds_test})
output.to_csv('/workspace/result.csv', index=False)
print('Predictions have been saved to result.csv.')
