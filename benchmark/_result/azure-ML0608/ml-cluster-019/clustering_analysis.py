import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Load the data from CSV files with the correct encoding
df_2009_2010 = pd.read_csv('Year 2009-2010.csv', encoding='ISO-8859-1')
df_2010_2011 = pd.read_csv('Year 2010-2011.csv', encoding='ISO-8859-1')

# Combine the datasets
df = pd.concat([df_2009_2010, df_2010_2011], ignore_index=True)

# Preprocessing
# Remove rows with missing Customer ID
df = df.dropna(subset=['Customer ID'])

# Convert InvoiceDate to datetime and extract possible useful features
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Year'] = df['InvoiceDate'].dt.year
df['Month'] = df['InvoiceDate'].dt.month
df['Day'] = df['InvoiceDate'].dt.day
df['Hour'] = df['InvoiceDate'].dt.hour

# Aggregate data to customer level
customer_data = df.groupby('Customer ID').agg({
    'Quantity': 'sum',
    'Price': 'mean',
    'Year': 'nunique',
    'Month': 'nunique',
    'Day': 'nunique',
    'Hour': 'nunique',
    'Country': 'first'  # Assume the first country is the primary country
}).reset_index(drop=True)

# Encode the 'Country' column
label_encoder = LabelEncoder()
customer_data['Country'] = label_encoder.fit_transform(customer_data['Country'])

# Define numerical and categorical features
numerical_features = ['Quantity', 'Price', 'Year', 'Month', 'Day', 'Hour']
categorical_features = ['Country']

# Create preprocessing pipelines
numerical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

preprocessor = ColumnTransformer([
    ('num', numerical_pipeline, numerical_features),
    ('cat', 'passthrough', categorical_features)
])

# Preprocess the data
X = preprocessor.fit_transform(customer_data)

# Clustering
kmeans = KMeans(n_clusters=5, random_state=42)
customer_data['Cluster'] = kmeans.fit_predict(X)

# Save the processed features and cluster labels to a CSV file
processed_features = pd.DataFrame(X, columns=[f'Processed_Feature_{i}' for i in range(X.shape[1])])
processed_features['Cluster'] = customer_data['Cluster']
processed_features.to_csv('cluster.csv', index=False)
