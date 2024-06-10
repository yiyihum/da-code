import pandas as pd

# Load the dataset
df = pd.read_csv('/workspace/world-data-2023.csv')

# Select columns that are relevant for clustering and can be converted to numeric
numeric_columns = [
    'Density\n(P/Km2)', 'Agricultural Land( %)', 'Land Area(Km2)', 'Armed Forces size',
    'Birth Rate', 'Fertility Rate', 'Infant mortality', 'Life expectancy',
    'Maternal mortality ratio', 'Physicians per thousand', 'Latitude', 'Longitude'
]

# Convert columns to numeric, coercing errors to NaN (not a number)
for col in numeric_columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.replace(',', '').str.strip()
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Display the number of NaN values in each column
nan_counts = df[numeric_columns].isna().sum()
print(nan_counts)
