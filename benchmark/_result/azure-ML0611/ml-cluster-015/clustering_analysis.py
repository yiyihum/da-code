import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('/workspace/77_cancer_proteomes_CPTAC_itraq.csv')

# Drop non-numeric columns
df_numeric = df.drop(columns=['RefSeq_accession_number', 'gene_symbol', 'gene_name'])

# Impute missing values with the mean of the column
imputer = SimpleImputer(strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df_numeric), columns=df_numeric.columns)

# Standardize the features
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_imputed), columns=df_imputed.columns)

# Apply KMeans clustering
# The README mentioned that the best clustering in the original study was achieved using 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)
df_scaled['Cluster'] = kmeans.fit_predict(df_scaled)

# Prepare the output dataframe
output_df = pd.DataFrame(df_scaled['Cluster'], columns=['Cluster'])
for i, column in enumerate(df_scaled.columns[:-1]):
    output_df.loc[:, f'Processed_Feature_{i}'] = df_scaled[column]

# Save the clustering results to a CSV file
output_df.to_csv('/workspace/cluster.csv', index=False)
