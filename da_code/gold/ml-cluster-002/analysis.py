import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

wine = pd.read_csv("../wine-clustering.csv")

pca = PCA(n_components=2)
wine_pca = pca.fit_transform(wine)
wine_pca = pd.DataFrame(wine_pca, columns=["Feature_1", "Feature_2"])

kmeans = KMeans(n_clusters=3)
wine_pca["Cluster"] = kmeans.fit_predict(wine_pca)

silhouette_avg = silhouette_score(wine_pca[["Feature_1", "Feature_2"]], wine_pca["Cluster"])
print(f'Silhouette Score: {silhouette_avg:.3f}')
wine_pca.to_csv("./result.csv", index=False)

