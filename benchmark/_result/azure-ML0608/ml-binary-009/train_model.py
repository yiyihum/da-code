import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# Load the training data
train_df = pd.read_csv('/workspace/train.csv')

# Preprocess the training data
train_df['Arrival Delay in Minutes'].fillna(train_df['Arrival Delay in Minutes'].median(), inplace=True)
train_df.drop(columns=['Unnamed: 0', 'id'], inplace=True)

# Encode categorical variables
categorical_cols = ['Gender', 'Customer Type', 'Type of Travel', 'Class']
label_encoders = {}
for col in categorical_cols:
    label_encoders[col] = LabelEncoder()
    train_df[col] = label_encoders[col].fit_transform(train_df[col])

# Split the data into features and target
X_train = train_df.drop('satisfaction', axis=1)
y_train = train_df['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the model and label encoders for later use
import joblib
joblib.dump(model, '/workspace/satisfaction_model.pkl')
for col, le in label_encoders.items():
    joblib.dump(le, f'/workspace/{col}_encoder.pkl')

print("Model training complete.")
