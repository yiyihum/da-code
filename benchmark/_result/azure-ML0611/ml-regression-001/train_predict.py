import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# Load the training data
train_data = pd.read_csv('/workspace/Clean_Dataset.csv')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Drop the 'Unnamed: 0' column as it is just an identifier
train_data.drop('Unnamed: 0', axis=1, inplace=True)
test_data.drop('Unnamed: 0', axis=1, inplace=True)

# Separate the target variable and features for training data
X_train = train_data.drop('price', axis=1)
y_train = train_data['price']

# List of categorical columns
categorical_cols = [cname for cname in X_train.columns if
                    X_train[cname].dtype == "object"]

# List of numerical columns
numerical_cols = [cname for cname in X_train.columns if 
                  X_train[cname].dtype in ['int64', 'float64']]

# Preprocessing for numerical data
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)])

# Create and train the model
model = Pipeline(steps=[('preprocessor', preprocessor),
                        ('model', LinearRegression())])

model.fit(X_train, y_train)

# Preprocess the test data and predict the prices
predicted_prices = model.predict(test_data)

# Save the predictions to a CSV file
result = pd.DataFrame({'price': predicted_prices})
result.to_csv('/workspace/result.csv', index=False)
print("Prediction completed and saved to result.csv")
