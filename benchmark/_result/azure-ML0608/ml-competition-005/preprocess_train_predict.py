import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import log_loss
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the datasets
train_data = pd.read_csv('/workspace/train.csv')
test_data = pd.read_csv('/workspace/test.csv')

# Separate features and target from the training data
X = train_data.drop(['Status', 'id'], axis=1)
y = train_data['Status']

# One-hot encode the categorical variables
categorical_features = ['Drug', 'Sex', 'Ascites', 'Hepatomegaly', 'Spiders', 'Edema']
numerical_features = X.select_dtypes(include=['int64', 'float64']).columns

# Create the preprocessing pipeline for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', numerical_features),
        ('cat', OneHotEncoder(), categorical_features)
    ])

# Create the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Create the pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, y_train)

# Validate the model
y_val_pred = pipeline.predict_proba(X_val)
val_log_loss = log_loss(y_val, y_val_pred)
print(f"Validation Log Loss: {val_log_loss}")

# Prepare the test data
test_X = test_data.drop('id', axis=1)

# Make predictions on the test data
test_predictions = pipeline.predict_proba(test_X)

# Create the submission dataframe
submission = pd.DataFrame(test_predictions, columns=pipeline.classes_)
submission.insert(0, 'id', test_data['id'])

# Save the submission file
submission.to_csv('/workspace/submission.csv', index=False)
print("Submission file saved.")
