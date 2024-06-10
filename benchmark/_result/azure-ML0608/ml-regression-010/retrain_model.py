import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

# Load the training data
train_data = pd.read_csv('/workspace/drugsComTrain_raw.csv')

# Preprocessing
# Clean the review text
train_data['clean_review'] = train_data['review'].str.replace(r"[^a-zA-Z\s]", "", regex=True).str.lower()

# Feature extraction from text
tfidf = TfidfVectorizer(max_features=100)  # Use the same number of features as before
tfidf_matrix = tfidf.fit_transform(train_data['clean_review'])

# Train a linear regression model using only the TF-IDF features
X_train, X_val, y_train, y_val = train_test_split(tfidf_matrix, train_data['usefulCount'], test_size=0.2, random_state=42)
regressor = LinearRegression()
regressor.fit(X_train, y_train)

# Validate the model
y_pred = regressor.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
print(f"Mean Squared Error: {mse}")

# Save the retrained model and the tfidf vectorizer for later use
joblib.dump(regressor, '/workspace/usefulness_linear_regressor_tf_only.joblib')
joblib.dump(tfidf, '/workspace/tfidf_vectorizer_tf_only.joblib')
