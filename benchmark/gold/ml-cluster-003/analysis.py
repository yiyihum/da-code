import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 加载数据
clusteringdata = pd.read_csv('../New_York_cars.csv')

features = ['Exterior color', 'Interior color', 'Drivetrain', 'Fuel type', 'Transmission',
            'Engine', 'Mileage', 'Safety', 'Year', 'Model']

clusteringdata = clusteringdata[features]  
clusteringdata['Engine'] = clusteringdata['Engine'].str.extract(r'(\d+\.?\d*)').astype(float)
clusteringdata = clusteringdata.dropna(subset=['Engine']) 
sample_size = 10000
if clusteringdata.shape[0] > sample_size:
    clusteringdata = clusteringdata.sample(n=sample_size, random_state=42)
large_values = ['Engine', 'Mileage']
for column in large_values:
    if clusteringdata[column].max() > 1000:
        clusteringdata[column] = clusteringdata[column] / 1000
categorical_cols = ['Exterior color', 'Interior color', 'Drivetrain', 'Fuel type', 'Transmission', 'Safety']
clusteringdata_encoded = pd.get_dummies(clusteringdata, columns=categorical_cols)
clusteringdata_encoded = clusteringdata_encoded.drop('Model', axis=1)
scaler = StandardScaler()
numerical_cols = ['Engine', 'Mileage', 'Year']
clusteringdata_encoded[numerical_cols] = scaler.fit_transform(clusteringdata_encoded[numerical_cols])
clusteringdata_encoded = clusteringdata_encoded.replace([np.inf, -np.inf], np.nan)
clusteringdata_encoded = clusteringdata_encoded.dropna()
clusteringdata_encoded = clusteringdata_encoded.iloc[:, :3]

pca = PCA(n_components=0.95)
clusteringdata_reduced = pca.fit_transform(clusteringdata_encoded)

# Create the DBSCAN clustering model
dbscan = DBSCAN(eps=0.5, min_samples=5, n_jobs=-1)
dbscan.fit(clusteringdata_reduced)
# Get the cluster labels for each data point
cluster_labels = dbscan.labels_


# Create a DataFrame to store the results
result = pd.DataFrame(clusteringdata_reduced, columns=[f'Feature_{i+1}' for i in range(clusteringdata_reduced.shape[1])])
# Add the cluster labels to the DataFrame
result['Cluster'] = cluster_labels

result.to_csv('./clustering.csv', index=False)

