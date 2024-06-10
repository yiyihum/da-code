import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the training data
train_data = pd.read_csv('/workspace/data.csv')

# Separate the features and target variable
X_train = train_data.drop('AVG_JOB_SATISFACTION', axis=1)
y_train = train_data['AVG_JOB_SATISFACTION']

# Define categorical columns
categorical_cols = ['GEO', 'COUNTRY']

# Define numerical columns
numerical_cols = [cname for cname in X_train.columns if 
                  X_train[cname].dtype in ['int64', 'float64'] and 
                  cname not in categorical_cols]

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
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Define the model
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Bundle preprocessing and modeling code in a pipeline
my_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                              ('model', model)])

# Preprocessing of training data, fit model 
my_pipeline.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocessing of test data, get predictions
predictions = my_pipeline.predict(test_data)

# Save the predictions to a new CSV file
output = pd.DataFrame({'AVG_JOB_SATISFACTION': predictions})
output.to_csv('/workspace/job_satisfaction.csv', index=False)
