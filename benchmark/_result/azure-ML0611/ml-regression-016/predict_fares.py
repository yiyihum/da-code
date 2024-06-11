import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Function to preprocess data
def preprocess_data(data, label_encoders=None, train=True):
    # Convert 'Date_of_journey' into datetime and extract day, month, year
    data['Date_of_journey'] = pd.to_datetime(data['Date_of_journey'])
    data['Journey_day'] = data['Date_of_journey'].dt.day
    data['Journey_month'] = data['Date_of_journey'].dt.month
    data['Journey_year'] = data['Date_of_journey'].dt.year
    data.drop('Date_of_journey', axis=1, inplace=True)
    
    # Encode categorical variables
    if train:
        label_encoders = {}
        for column in ['Airline', 'Flight_code', 'Class', 'Source', 'Departure', 'Total_stops', 'Arrival', 'Destination']:
            le = LabelEncoder()
            data[column] = le.fit_transform(data[column])
            label_encoders[column] = le
    else:
        for column in ['Airline', 'Flight_code', 'Class', 'Source', 'Departure', 'Total_stops', 'Arrival', 'Destination']:
            le = label_encoders[column]
            # Handle unseen labels by assigning a unique value
            data[column] = data[column].map(lambda s: 'Unknown' if s not in le.classes_ else s)
            le_classes = le.classes_.tolist()
            if 'Unknown' not in le_classes:
                le_classes.append('Unknown')
            le.classes_ = np.array(le_classes)
            data[column] = le.transform(data[column])
    
    return data, label_encoders

# Load the training data
train_data = pd.read_csv('/workspace/Cleaned_dataset.csv')

# Preprocess the training data
train_data, label_encoders = preprocess_data(train_data)

# Separate features and target
X_train = train_data.drop('Fare', axis=1)
y_train = train_data['Fare']

# Train the model with a minimal number of estimators to reduce training time
model = RandomForestRegressor(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Preprocess the test data using the same preprocessing steps and label encoders
test_data, _ = preprocess_data(test_data, label_encoders, train=False)

# Predict the fares
predictions = model.predict(test_data)

# Save the predictions
prediction_df = pd.DataFrame(predictions, columns=['Fare'])
prediction_df.to_csv('/workspace/fare.csv', index=False)
