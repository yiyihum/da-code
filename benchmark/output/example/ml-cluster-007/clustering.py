import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('/workspace/03_Clustering_Marketing.csv')

# Handle missing values
# Replace 'NA' with NaN and convert the 'age' column to numeric, coercing errors to NaN
df.replace('NA', pd.NA, inplace=True)
df['age'] = pd.to_numeric(df['age'], errors='coerce')

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df.select_dtypes(include='number')), columns=df.select_dtypes(include='number').columns)

# Normalize the data
scaler = StandardScaler()
df_normalized = scaler.fit_transform(df_imputed)

# Apply KMeans clustering
kmeans = KMeans(n_clusters=5, random_state=42)
df_imputed['Cluster'] = kmeans.fit_predict(df_normalized)

# Prepare the dataframe for output
output_df = df_imputed.copy()
output_df.columns = ['Feature_' + str(i) if i < len(output_df.columns) - 1 else 'Cluster' for i in range(len(output_df.columns))]

# Save the clustering results to cluster.csv
output_df.to_csv('/workspace/cluster.csv', index=False)
