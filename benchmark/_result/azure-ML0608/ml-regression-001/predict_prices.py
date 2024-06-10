import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer

# Load the datasets
train_data = pd.read_csv('/workspace/Clean_Dataset.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Drop the 'Unnamed: 0' column as it's just an index
train_data.drop(columns=['Unnamed: 0'], inplace=True)
test_data.drop(columns=['Unnamed: 0'], inplace=True)

# Separate features and target from training data
X_train = train_data.drop(columns=['price'])
y_train = train_data['price']

# Preprocessing for categorical data
categorical_cols = [cname for cname in X_train.columns if
                    X_train[cname].dtype == "object"]

# Preprocessing for numerical data
numerical_cols = [cname for cname in X_train.columns if 
                  X_train[cname].dtype in ['int64', 'float64']]

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', SimpleImputer(strategy='mean'), numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Create and train the model
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('model', LinearRegression())])

model.fit(X_train, y_train)

# Predict on the test data
test_preds = model.predict(test_data)

# Save the predictions to a CSV file
result = pd.DataFrame(test_preds, columns=['price'])
result.to_csv('/workspace/result.csv', index=False)
