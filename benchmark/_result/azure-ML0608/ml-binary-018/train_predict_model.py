import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the training dataset
train_data = pd.read_csv('/workspace/healthcare-dataset-stroke-data.csv')

# Separate features and target variable
X = train_data.drop(['id', 'stroke'], axis=1)
y = train_data['stroke']

# Preprocessing for numerical data
numerical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Preprocessing for categorical data
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Bundle preprocessing for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numerical_transformer, ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi']),
        ('cat', categorical_transformer, ['gender', 'ever_married', 'work_type', 'Residence_type', 'smoking_status'])
    ])

# Define the model
model = LogisticRegression(max_iter=1000)

# Create and evaluate the pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])

# Split data into train and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

# Preprocessing of training data, fit model
pipeline.fit(X_train, y_train)

# Preprocessing of validation data, get predictions
preds = pipeline.predict(X_valid)

# Evaluate the model
score = accuracy_score(y_valid, preds)
print('Accuracy:', score)

# Save the model to disk
import joblib
joblib.dump(pipeline, 'stroke_model.pkl')

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Drop the 'id' column as it's not a feature
test_data = test_data.drop(['id'], axis=1)

# Make predictions on the test data
test_preds = pipeline.predict(test_data)

# Save the predictions to a CSV file
output = pd.DataFrame({'stroke': test_preds})
output.to_csv('/workspace/stroke.csv', index=False)
print('Prediction on test data saved to stroke.csv')
