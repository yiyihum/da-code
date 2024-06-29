import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Remove the duplicate 'id' column
train_data = train_data.loc[:, ~train_data.columns.duplicated()]

# Split the data into features and target variables
X = train_data.drop(columns=['id', 'Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults'])
y = train_data[['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']]

# Split the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Perform cross-validation to evaluate the model
cv_scores = cross_val_score(rf_classifier, X_train, y_train, cv=5)

# Train the Random Forest Classifier
rf_classifier.fit(X_train, y_train)

# Predict on the validation set
y_pred = rf_classifier.predict(X_val)

# Calculate the accuracy on the validation set
accuracy = accuracy_score(y_val, y_pred)

# Print the cross-validation scores and validation accuracy
print(f'Cross-validation scores: {cv_scores}')
print(f'Validation accuracy: {accuracy}')
