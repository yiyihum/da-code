import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_data = pd.read_csv('mushrooms.csv')

# Preprocess the data: Label encoding for categorical variables
label_encoders = {}
for column in train_data.columns:
    if train_data[column].dtype == 'object':
        le = LabelEncoder()
        train_data[column] = le.fit_transform(train_data[column])
        label_encoders[column] = le

# Separate features and target
X = train_data.drop('class', axis=1)
y = train_data['class']

# Train a Random Forest Classifier
clf = RandomForestClassifier(random_state=42)
clf.fit(X, y)

# Load the test data
test_data = pd.read_csv('test.csv')

# Preprocess the test data using the same label encoders
for column in test_data.columns:
    if test_data[column].dtype == 'object':
        le = label_encoders[column]
        test_data[column] = le.transform(test_data[column])

# Predict the class for the test data
predictions = clf.predict(test_data)

# Save the predictions to a new file
predictions_df = pd.DataFrame(predictions, columns=['class'])
predictions_df.to_csv('class.csv', index=False)
