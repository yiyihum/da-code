import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import log_loss

# Load the training data
train_data = pd.read_csv('/workspace/train.csv')

# Remove the duplicate 'id.1' column
train_data.drop(columns=['id.1'], inplace=True)

# Combine the target variables into a single binary class
condition_columns = ['Pastry', 'Z_Scratch', 'K_Scatch', 'Stains', 'Dirtiness', 'Bumps', 'Other_Faults']
train_data['Class'] = train_data[condition_columns].max(axis=1)
train_data.drop(columns=condition_columns, inplace=True)

# Split the data into features and labels
X = train_data.drop(columns=['Class', 'id'])
y = train_data['Class']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf_classifier.fit(X_train, y_train)

# Validate the model
y_val_pred = rf_classifier.predict_proba(X_val)
val_log_loss = log_loss(y_val, y_val_pred)

# Output the validation log loss
print(f"Validation Log Loss: {val_log_loss}")
