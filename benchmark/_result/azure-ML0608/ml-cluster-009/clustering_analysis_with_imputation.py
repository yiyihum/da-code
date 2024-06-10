import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('/workspace/world-data-2023.csv')

# Select columns that are relevant for clustering and can be converted to numeric
# Excluding 'Agricultural Land( %)' due to no observed values
numeric_columns = [
    'Density\n(P/Km2)', 'Land Area(Km2)', 'Armed Forces size',
    'Birth Rate', 'Fertility Rate', 'Infant mortality', 'Life expectancy',
    'Maternal mortality ratio', 'Physicians per thousand', 'Latitude', 'Longitude'
]

# Convert columns to numeric, coercing errors to NaN (not a number)
for col in numeric_columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace(',', '').str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Impute missing values with the median for the remaining columns
imputer = SimpleImputer(strategy='median')
df[numeric_columns] = imputer.fit_transform(df[numeric_columns])

# Standardize the data
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[numeric_columns])

# Perform K-Means clustering with 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_scaled)

# Prepare the output dataframe with processed features and cluster labels
output_columns = ['Processed_Feature_' + str(i) for i in range(df_scaled.shape[1])] + ['Cluster']
output_df = pd.DataFrame(df_scaled, columns=output_columns[:len(numeric_columns)])
output_df['Cluster'] = df['Cluster'].values

# Save the clustering results to a CSV file
output_df.to_csv('/workspace/cluster.csv', index=False)
