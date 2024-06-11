import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load the cleaned training data
train_data = pd.read_csv('/workspace/clean_train.csv')

# Separate features and target variable
X = train_data.drop('NObeyesdad', axis=1)
y = train_data['NObeyesdad']

# List of categorical columns to be one-hot encoded
categorical_cols = [cname for cname in X.columns if X[cname].dtype == "object"]

# List of numerical columns
numerical_cols = [cname for cname in X.columns if X[cname].dtype in ['int64', 'float64']]

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

# Split data into training and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# Preprocess the data
X_train = preprocessor.fit_transform(X_train)
X_valid = preprocessor.transform(X_valid)

# Output the shape of the processed feature data
print("X_train shape:", X_train.shape)
print("X_valid shape:", X_valid.shape)
