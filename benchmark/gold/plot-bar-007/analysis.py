import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

listings_df = pd.read_csv("../listings.csv")
listings_df = listings_df.T.drop_duplicates().T
listings_df.dropna(axis=1, how='all', inplace=True)
listings_df.drop([c for c in listings_df.columns if listings_df[c].nunique()==1], axis=1, inplace=True)
listings_df.drop(listings_df.columns[listings_df.columns.str.contains("url")], axis=1, inplace=True)
listings_df.price = listings_df.price.str.replace(r"$", "").str.replace(",", "").astype("float32")
listings_df.weekly_price = listings_df.weekly_price.str.replace(r"$", "").str.replace(",", "").astype("float32")
listings_df.monthly_price = listings_df.monthly_price.str.replace(r"$", "").str.replace(",", "").astype("float32")
listings_df.security_deposit = listings_df.security_deposit.str.replace(r"$", "").str.replace(",", "").astype("float32")
listings_df.cleaning_fee = listings_df.cleaning_fee.str.replace(r"$", "").str.replace(r"$", "").str.replace(",", "").astype("float32")
listings_df.extra_people = listings_df.extra_people.str.replace(r"$","").str.replace(",","").astype("float32")
columns_to_drop = [
    'square_feet', 'summary', 'space', 'neighborhood_overview', 'notes', 'transit',
]

# Dropping host-related information (selecting by pattern)
host_related_columns = listings_df.columns[listings_df.columns.str.contains('^host_')]
columns_to_drop.extend(host_related_columns)

# Dropping the columns
listings_df.drop(columns=columns_to_drop, inplace=True)
numerical_columns = listings_df.select_dtypes(exclude=object).columns.tolist()
categorical_columns = listings_df.select_dtypes(include=object).columns.tolist()

numeric_imputer = SimpleImputer(strategy='median')
listings_df[numerical_columns] = numeric_imputer.fit_transform(listings_df[numerical_columns])

# Categorical columns with mode imputation
categorical_imputer = SimpleImputer(strategy='most_frequent')
                                    
# Estimating occupancy rates
average_annual_availability = listings_df['availability_365'].mean()
estimated_annual_occupancy_rate = 100 - (average_annual_availability / 365 * 100)

neighborhood_counts = listings_df['neighbourhood_group_cleansed'].value_counts().head(10) # Calculate the distribution of listings by neighborhood

# Create a bar chart for the top neighborhoods with the most listings
plt.figure(figsize=(16, 8))
sns.barplot(x=neighborhood_counts.index, y=neighborhood_counts.values, palette="coolwarm")
plt.title('Top 10 Neighborhoods by Number of Listings')
plt.xlabel('Neighborhood')
plt.ylabel('Number of Listings')
plt.savefig('./result.png')