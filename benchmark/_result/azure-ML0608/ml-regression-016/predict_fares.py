import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer

# Load the training data
train_data = pd.read_csv('/workspace/Cleaned_dataset.csv')

# Separate features and target
X_train = train_data.drop('Fare', axis=1)
y_train = train_data['Fare']

# Define categorical columns
categorical_columns = X_train.select_dtypes(include=['object']).columns

# Create a ColumnTransformer with OneHotEncoder for categorical features
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns)
    ],
    remainder='passthrough'  # Leave the rest of the columns untouched
)

# Fit the preprocessor and transform the training data
X_train = preprocessor.fit_transform(X_train)

# Train a Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Transform the test data using the same preprocessor
X_test = preprocessor.transform(test_data)

# Predict the fares for the test data
test_data['Fare'] = model.predict(X_test)

# Save the predictions to a new CSV file
test_data[['Fare']].to_csv('/workspace/fare.csv', index=False)
