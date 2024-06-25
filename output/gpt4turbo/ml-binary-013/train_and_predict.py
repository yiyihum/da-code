import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('Train.csv')
test_data = pd.read_csv('Test.csv')

# Separate features and target
X_train = train_data.drop('Target', axis=1)
y_train = train_data['Target']

# Create a pipeline with imputation of missing values and scaling
pipeline = make_pipeline(
    SimpleImputer(strategy='mean'),
    StandardScaler(),
    LogisticRegression(max_iter=1000)
)

# Train the model using the pipeline
pipeline.fit(X_train, y_train)

# Preprocess the test data and make predictions using the pipeline
predictions = pipeline.predict(test_data)

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(predictions, columns=['Target'])
predictions_df.to_csv('target.csv', index=False)
