import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Load the dataset
df = pd.read_csv('New_York_cars.csv')

# Preprocessing
# For simplicity, let's consider only numerical features for clustering
numerical_features = ['money', 'MPG', 'Mileage', 'Year']
df_numerical = df[numerical_features].copy()

# Convert MPG to numerical by taking the average of the range
def process_mpg(mpg_value):
    try:
        mpg_range = mpg_value.split('–')
        if len(mpg_range) == 2:
            return (float(mpg_range[0]) + float(mpg_range[1])) / 2
        else:
            return float(mpg_value)
    except:
        return None

df_numerical['MPG'] = df_numerical['MPG'].apply(process_mpg)

# Drop rows with any missing values
df_numerical.dropna(inplace=True)

# Standardize the numerical features
scaler = StandardScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df_numerical), columns=df_numerical.columns)

# Clustering
kmeans = KMeans(n_clusters=5, random_state=42)
df_scaled['Cluster'] = kmeans.fit_predict(df_scaled)

# Save the clustering results
df_scaled.to_csv('cluster.csv', index=False)
