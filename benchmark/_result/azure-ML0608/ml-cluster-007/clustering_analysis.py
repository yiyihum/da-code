import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('03_Clustering_Marketing.csv')

# Handle missing values
# Replace 'NA' with NaN and convert the 'age' column to numeric, forcing errors to NaN
df.replace('NA', pd.NA, inplace=True)
df['age'] = pd.to_numeric(df['age'], errors='coerce')

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df.select_dtypes(include='number')), columns=df.select_dtypes(include='number').columns)

# Normalize the data
scaler = StandardScaler()
df_normalized = pd.DataFrame(scaler.fit_transform(df_imputed), columns=df_imputed.columns)

# Perform k-means clustering
kmeans = KMeans(n_clusters=5, random_state=42)
df_normalized['Cluster'] = kmeans.fit_predict(df_normalized)

# Prepare the final dataframe with processed features and cluster labels
final_df = pd.concat([df_normalized, df.select_dtypes(exclude='number')], axis=1)

# Save the clustering results to a CSV file
final_df.to_csv('cluster.csv', index=False)
