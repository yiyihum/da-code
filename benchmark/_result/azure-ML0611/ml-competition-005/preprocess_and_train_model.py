import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import log_loss
import numpy as np

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Separate features and target variable
X = train_data.drop(['id', 'Status'], axis=1)
y = train_data['Status']

# Encode target variable
status_mapping = {'C': 0, 'CL': 1, 'D': 2}
y_encoded = y.map(status_mapping)

# Identify categorical and numerical columns
categorical_cols = X.select_dtypes(include=['object']).columns
numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns

# Create the preprocessing pipelines for both numeric and categorical data
numeric_transformer = StandardScaler()
categorical_transformer = OneHotEncoder(handle_unknown='ignore')

# Combine preprocessing steps
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Create the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Create the pipeline
clf = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', model)])

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y_encoded, test_size=0.2, random_state=42)

# Train the model
clf.fit(X_train, y_train)

# Predict probabilities on the validation set
y_val_pred = clf.predict_proba(X_val)

# Calculate the log loss on the validation set
val_log_loss = log_loss(y_val, y_val_pred)
print(f"Validation Log Loss: {val_log_loss}")
