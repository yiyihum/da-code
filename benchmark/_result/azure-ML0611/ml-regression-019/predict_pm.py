from sklearn.cluster import KMeans
import pandas as pd

# Load the test data
test_data = pd.read_csv('/workspace/test.csv')

# Since we don't have the target variable 'pm', we will use a clustering approach
# We will use KMeans clustering to create clusters of the data points
kmeans = KMeans(n_clusters=10, random_state=0)

# Fit the model on the test data (excluding the 'profile_id' column)
kmeans.fit(test_data.drop('profile_id', axis=1))

# Assign the cluster centers as the predicted 'pm' values
test_data['pm'] = kmeans.predict(test_data.drop('profile_id', axis=1))

# Save the predicted 'pm' values to a CSV file
test_data[['pm']].to_csv('/workspace/pm.csv', index=False)
