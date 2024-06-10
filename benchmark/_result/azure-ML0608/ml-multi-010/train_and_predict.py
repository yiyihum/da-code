from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Load the training data
train_data = pd.read_csv('/workspace/bodyPerformance.csv')

# Encode the 'gender' categorical variable
le_gender = LabelEncoder()
train_data['gender'] = le_gender.fit_transform(train_data['gender'])

# Split the data into features and target variable
X = train_data.drop('class', axis=1)
y = train_data['class']

# Encode the target variable
le_class = LabelEncoder()
y_encoded = le_class.fit_transform(y)

# Initialize the Random Forest Classifier
rf_classifier = RandomForestClassifier(random_state=42)

# Train the model
rf_classifier.fit(X, y_encoded)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Apply the same encoding to the 'gender' variable in the test data
test_data['gender'] = le_gender.transform(test_data['gender'])

# Make predictions on the test data
predictions_encoded = rf_classifier.predict(test_data)

# Decode the predictions back to the original class labels
predictions = le_class.inverse_transform(predictions_encoded)

# Save the predictions to a new file named class.csv with the column name "class"
predictions_df = pd.DataFrame(predictions, columns=['class'])
predictions_df.to_csv('/workspace/class.csv', index=False)
