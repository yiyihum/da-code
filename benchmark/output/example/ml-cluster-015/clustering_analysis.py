import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the dataset
data = pd.read_csv('77_cancer_proteomes_CPTAC_itraq.csv')

# Drop non-numeric columns and the last three columns (healthy individuals)
data = data.drop(['RefSeq_accession_number', 'gene_symbol', 'gene_name'], axis=1)
data = data.iloc[:, :-3]

# Handle missing values by imputing with the mean
imputer = SimpleImputer(missing_values=pd.NA, strategy='mean')
data_imputed = pd.DataFrame(imputer.fit_transform(data), columns=data.columns)

# Normalize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_imputed)

# Perform K-means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(data_scaled)

# Add the cluster labels to the original data
data_imputed['Cluster'] = clusters

# Prepare the output dataframe with the required column names
output_df = pd.DataFrame(data_scaled, columns=[f'Feature_{i+1}' for i in range(data_scaled.shape[1])])
output_df['Cluster'] = clusters

# Save the clustering results to a CSV file
output_df.to_csv('cluster.csv', index=False)
