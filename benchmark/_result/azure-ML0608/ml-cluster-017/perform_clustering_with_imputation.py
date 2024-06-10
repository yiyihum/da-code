import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt

# Load the preprocessed dataset
df = pd.read_csv('/workspace/preprocessed_data.csv')

# Impute missing values with the mean
imputer = SimpleImputer(missing_values=pd.NA, strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

# Determine the optimal number of clusters using the elbow method
inertia = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=0).fit(df_imputed)
    inertia.append(kmeans.inertia_)

# Plot the elbow graph
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method For Optimal k')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()

# Choose the number of clusters (k) and perform K-Means clustering
# Here we assume the elbow is at k=3 for demonstration purposes
k = 3
kmeans = KMeans(n_clusters=k, random_state=0).fit(df_imputed)

# Add the cluster labels to the dataframe
df_imputed['Cluster'] = kmeans.labels_

# Save the clustering results to a CSV file
output_file = '/workspace/cluster.csv'
df_imputed.to_csv(output_file, index=False)

print(f'Clustering results saved to {output_file}')
