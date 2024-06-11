import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the datasets
train_data = pd.read_csv('/workspace/New_York_cars.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Impute missing values in the target column 'Mileage'
train_data['Mileage'].fillna(train_data['Mileage'].mean(), inplace=True)

# Separate the target variable and features in the training data
X_train = train_data.drop('Mileage', axis=1)
y_train = train_data['Mileage']

# Preprocessing for numerical data
numerical_transformer = SimpleImputer(strategy='constant')

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, X_train.select_dtypes(exclude=['object']).columns),
        ('cat', categorical_transformer, X_train.select_dtypes(include=['object']).columns)
    ])

# Define the model with fewer estimators to reduce complexity
model = RandomForestRegressor(n_estimators=10, random_state=0)

# Bundle preprocessing and modeling code in a pipeline
my_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('model', model)
                             ])

# Preprocessing of training data, fit model
my_pipeline.fit(X_train, y_train)

# Preprocessing of test data, get predictions
preds = my_pipeline.predict(test_data)

# Save the predictions to a CSV file
output = pd.DataFrame({'Mileage': preds})
output.to_csv('/workspace/result.csv', index=False)
