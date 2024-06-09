import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# Load the training data
train_data = pd.read_csv('onlinefoods.csv')

# Preprocess the data: select relevant columns and drop rows with missing values
train_data = train_data[['Feedback']].dropna()

# Split the data into features and target
X_train = train_data['Feedback']
y_train = train_data['Feedback'].apply(lambda x: 'Positive' if 'Positive' in x else 'Negative')

# Create a model pipeline
model = make_pipeline(CountVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('test.csv')

# Since we don't have the 'Feedback' column in test data, we'll use a dummy column with empty strings
test_data['Feedback'] = ['' for _ in range(len(test_data))]

# Make predictions
predictions = model.predict(test_data['Feedback'])

# Write the predictions into 'result.csv'
result_df = pd.DataFrame(predictions, columns=['result'])
result_df.to_csv('result.csv', index=False)
