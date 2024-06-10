import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('/workspace/77_cancer_proteomes_CPTAC_itraq.csv')

# Drop non-numeric columns and the last three columns (healthy individuals)
df_numeric = df.drop(columns=['RefSeq_accession_number', 'gene_symbol', 'gene_name'])
df_numeric = df_numeric.iloc[:, :-3]

# Handle missing values by imputing with the mean
imputer = SimpleImputer(missing_values=pd.NA, strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df_numeric), columns=df_numeric.columns)

# Standardize the features
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_imputed), columns=df_imputed.columns)

# Perform K-means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df_scaled['Cluster'] = kmeans.fit_predict(df_scaled)

# Prepare the dataframe for saving
df_result = df_scaled.copy()
df_result.columns = [f'Processed_Feature_{i}' if i != len(df_result.columns) - 1 else 'Cluster' for i in range(len(df_result.columns))]

# Save the clustering results to a CSV file
df_result.to_csv('/workspace/cluster.csv', index=False)
