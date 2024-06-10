import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the dataset
data = pd.read_csv('/workspace/Country-data.csv')

# Drop the 'country' column as it's not needed for clustering
data_features = data.drop('country', axis=1)

# Initialize the StandardScaler
scaler = StandardScaler()

# Fit and transform the data features
scaled_features = scaler.fit_transform(data_features)

# Convert the scaled features back to a DataFrame
scaled_data = pd.DataFrame(scaled_features, columns=data_features.columns)

# Save the scaled data to a CSV file for further use
scaled_data.to_csv('/workspace/scaled_data.csv', index=False)

print("Data scaling complete and saved to scaled_data.csv.")
