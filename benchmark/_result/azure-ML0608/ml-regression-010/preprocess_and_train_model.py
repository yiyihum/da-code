import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the training data
train_data = pd.read_csv('/workspace/drugsComTrain_raw.csv')

# Preprocessing
# Clean the review text
train_data['clean_review'] = train_data['review'].str.replace(r"[^a-zA-Z\s]", "", regex=True).str.lower()

# Encode categorical variables
le_drug = LabelEncoder()
train_data['drug_encoded'] = le_drug.fit_transform(train_data['drugName'])

le_condition = LabelEncoder()
train_data['condition_encoded'] = le_condition.fit_transform(train_data['condition'].astype(str))

# Feature extraction from text
tfidf = TfidfVectorizer(max_features=100)  # Further reduced number of features
tfidf_matrix = tfidf.fit_transform(train_data['clean_review'])

# Combine all features
X = np.hstack((tfidf_matrix.toarray(), train_data[['drug_encoded', 'condition_encoded', 'rating']].values))
y = train_data['usefulCount']

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a linear regression model
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Validate the model
y_pred = regressor.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
print(f"Mean Squared Error: {mse}")

# Save the model and encoders for later use
import joblib
joblib.dump(regressor, '/workspace/usefulness_linear_regressor.joblib')
joblib.dump(le_drug, '/workspace/drug_encoder.joblib')
joblib.dump(le_condition, '/workspace/condition_encoder.joblib')
joblib.dump(tfidf, '/workspace/tfidf_vectorizer.joblib')
