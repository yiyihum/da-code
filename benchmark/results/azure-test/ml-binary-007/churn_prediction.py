import csv
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Function to load data and preprocess
def load_data(filename, is_training_data=True):
    data = []
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)
    return data

# Function to preprocess the data
def preprocess_data(data, is_training_data=True):
    # Convert data to a format suitable for training
    # For simplicity, we will label encode categorical features
    # and convert all columns to float except for the target
    features = []
    targets = []
    label_encoders = {}
    for row in data:
        processed_row = []
        for key, value in row.items():
            if key in ['Gender', 'Subscription Type', 'Contract Length']:
                if key not in label_encoders:
                    label_encoders[key] = LabelEncoder()
                    label_encoders[key].fit([d[key] for d in data])
                processed_row.append(label_encoders[key].transform([value])[0])
            elif key == 'Churn' and is_training_data:
                targets.append(int(value))
            else:
                processed_row.append(float(value))
        features.append(processed_row)
    return features, targets, label_encoders

# Load and preprocess training data
train_data = load_data('customer_churn_dataset-training-master.csv')
train_features, train_targets, encoders = preprocess_data(train_data)

# Train model
model = LogisticRegression()
model.fit(train_features, train_targets)

# Load and preprocess testing data
test_data = load_data('customer_churn_dataset-testing-master.csv', False)
test_features, _, _ = preprocess_data(test_data, False)

# Make predictions
predictions = model.predict(test_features)

# Write predictions to a CSV file
with open('result.csv', 'w', newline='') as csvfile:
    fieldnames = ['result']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for prediction in predictions:
        writer.writerow({'result': prediction})
