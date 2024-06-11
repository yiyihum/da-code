import pandas as pd
import joblib

# Load the test data
test_data = pd.read_csv('/workspace/Test.csv')

# Impute missing values with mean (using training data mean)
train_data = pd.read_csv('/workspace/Train.csv')
test_data.fillna(train_data.mean(), inplace=True)

# Load the trained Random Forest classifier
rf_classifier = joblib.load('/workspace/rf_classifier.joblib')

# Make predictions on the test data
predictions = rf_classifier.predict(test_data)

# Save the predictions to a CSV file
predictions_df = pd.DataFrame(predictions, columns=['Target'])
predictions_df.to_csv('/workspace/target.csv', index=False)
