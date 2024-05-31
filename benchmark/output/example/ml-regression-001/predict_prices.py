import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the model
model = joblib.load('flight_price_model.pkl')

# Load the test data
df_test = pd.read_csv('test.csv')

# Preprocess the test data
label_encoder = LabelEncoder()
categorical_features = ['airline', 'flight', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class']
for feature in categorical_features:
    df_test[feature] = label_encoder.fit_transform(df_test[feature])

# Predict the prices
df_test['price'] = model.predict(df_test)

# Write the prediction results into result.csv
df_test.to_csv('result.csv', index=False)