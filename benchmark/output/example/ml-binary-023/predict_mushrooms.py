import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

# Function to encode categorical features using LabelEncoder
def encode_features(train_df, test_df, columns):
    encoder = LabelEncoder()
    for column in columns:
        # Fit the encoder on the data from both train and test sets combined
        encoder.fit(pd.concat([train_df[column], test_df[column]], ignore_index=True))
        train_df[column] = encoder.transform(train_df[column])
        test_df[column] = encoder.transform(test_df[column])
    return train_df, test_df

# Load the dataset
df = pd.read_csv('/workspace/mushrooms.csv')

# Separate features and target
X = df.drop(columns=['class'])
y = df['class']

# Preprocess the data
# Handle missing values - replace '?' with np.nan and then impute
X.replace('?', np.nan, inplace=True)

# Convert DataFrame to NumPy array before imputation
X_numpy = X.to_numpy()

imputer = SimpleImputer(strategy='most_frequent')
X_imputed = imputer.fit_transform(X_numpy)

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')
test_df.replace('?', np.nan, inplace=True)
test_numpy = test_df.to_numpy()
test_imputed = imputer.transform(test_numpy)

# Encode categorical features
X_imputed_df = pd.DataFrame(X_imputed, columns=X.columns)
test_imputed_df = pd.DataFrame(test_imputed, columns=test_df.columns)

# Encode both the training and test sets together
X_encoded, test_encoded = encode_features(X_imputed_df, test_imputed_df, X.columns)

# Split the dataset into the train and test sets
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Initialize the Random Forest classifier
classifier = RandomForestClassifier(random_state=42)

# Train the classifier
classifier.fit(X_train, y_train)

# Make predictions on the test set
y_pred = classifier.predict(X_test)

# Evaluate the classifier
accuracy = accuracy_score(y_test, y_pred)
print(f'Model accuracy: {accuracy:.2f}')

# Make predictions on the actual test data
test_predictions = classifier.predict(test_encoded)

# Write the predicted classes into a new file
pd.DataFrame(test_predictions, columns=['class']).to_csv('/workspace/class.csv', index=False)
