import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load the dataset
df = pd.read_csv('/workspace/world-data-2023.csv')

# Select numerical features for clustering
# Convert percentages to floats and remove commas and other non-numeric characters from numbers
df['Agricultural Land (%)'] = df['Agricultural Land( %)'].str.rstrip('%').astype('float') / 100.0
df['Land Area (Km2)'] = df['Land Area(Km2)'].str.replace(',', '').astype('float')
df['Armed Forces size'] = df['Armed Forces size'].str.replace(',', '').astype('float')
df['Birth Rate'] = df['Birth Rate'].astype('float')
df['Co2-Emissions'] = df['Co2-Emissions'].str.replace(',', '').astype('float')
df['CPI'] = df['CPI'].str.replace(',', '').astype('float')
df['CPI Change (%)'] = df['CPI Change (%)'].str.rstrip('%').astype('float') / 100.0
df['Fertility Rate'] = df['Fertility Rate'].astype('float')
df['Forested Area (%)'] = df['Forested Area (%)'].str.rstrip('%').astype('float') / 100.0
df['GDP'] = df['GDP'].str.replace('"', '').str.replace(',', '').str.replace(' ', '').str.replace('$', '').astype('float')
df['Infant mortality'] = df['Infant mortality'].astype('float')
df['Life expectancy'] = df['Life expectancy'].astype('float')
df['Maternal mortality ratio'] = df['Maternal mortality ratio'].astype('float')
df['Population'] = df['Population'].str.replace(',', '').astype('float')
df['Population: Labor force participation (%)'] = df['Population: Labor force participation (%)'].str.rstrip('%').astype('float') / 100.0
df['Tax revenue (%)'] = df['Tax revenue (%)'].str.rstrip('%').astype('float') / 100.0
df['Total tax rate'] = df['Total tax rate'].str.rstrip('%').astype('float') / 100.0
df['Unemployment rate'] = df['Unemployment rate'].str.rstrip('%').astype('float') / 100.0
df['Urban_population'] = df['Urban_population'].str.replace(',', '').astype('float')

# Drop the non-numeric and processed columns
columns_to_drop = ['Country', 'Density\n(P/Km2)', 'Abbreviation', 'Agricultural Land( %)', 'Land Area(Km2)', 'Armed Forces size', 'Co2-Emissions', 'CPI Change (%)', 'Currency-Code', 'Forested Area (%)', 'Gasoline Price', 'Gross primary education enrollment (%)', 'Gross tertiary education enrollment (%)', 'Largest city', 'Minimum wage', 'Official language', 'Out of pocket health expenditure', 'Physicians per thousand', 'Population: Labor force participation (%)', 'Tax revenue (%)', 'Total tax rate', 'Unemployment rate', 'Urban_population', 'Latitude', 'Longitude', 'Capital/Major City', 'Calling Code']
df.drop(columns=columns_to_drop, inplace=True)

# Handle any missing values by filling with the mean
df.fillna(df.mean(), inplace=True)

# Standardize the data
scaler = StandardScaler()
df_scaled = scaler.fit_transform(df)

# Perform K-Means clustering
kmeans = KMeans(n_clusters=3, random_state=0)
df['Cluster'] = kmeans.fit_predict(df_scaled)

# Save the results to a CSV file
df.to_csv('/workspace/cluster.csv', index=False)
