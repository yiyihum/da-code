import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# Load the dataset
df = pd.read_csv('/workspace/world-data-2023.csv')

# Convert columns with numerical information from object to float
numerical_cols = ['Density\n(P/Km2)', 'Agricultural Land( %)', 'Land Area(Km2)', 'Co2-Emissions', 
                  'CPI', 'CPI Change (%)', 'Forested Area (%)', 'Gasoline Price', 'GDP', 
                  'Gross primary education enrollment (%)', 'Gross tertiary education enrollment (%)', 
                  'Out of pocket health expenditure', 'Population', 'Population: Labor force participation (%)', 
                  'Tax revenue (%)', 'Total tax rate', 'Unemployment rate', 'Urban_population']

for col in numerical_cols:
    df[col] = pd.to_numeric(df[col].str.replace(',', '').str.replace('%', ''), errors='coerce')

# Drop columns with all missing values
df.dropna(axis=1, how='all', inplace=True)

# Select numerical columns for clustering
features = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

# Impute missing values with the mean
imputer = SimpleImputer(strategy='mean')
df[features] = imputer.fit_transform(df[features])

# Standardize the features
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df[features])

# Perform K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_scaled)

# Prepare the dataframe for output
output_df = pd.DataFrame(df_scaled, columns=[f'Processed_Feature_{i}' for i in range(df_scaled.shape[1])])
output_df['Cluster'] = df['Cluster']

# Save the clustering results to a CSV file
output_df.to_csv('/workspace/cluster.csv', index=False)
