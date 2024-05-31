import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
mall_df = pd.read_csv('../Mall_Customers.csv')

X = mall_df.iloc[:, [3, 4]].values  
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

num_clusters = 5
agg_cluster = AgglomerativeClustering(n_clusters=num_clusters, linkage='ward')
agg_cluster.fit(X)

result = pd.DataFrame({'Feature 1': X[:, 0], 'Feature 2': X[:, 1], 'Cluster': agg_cluster.labels_})
result.to_csv('./cluster.csv', index=False)

