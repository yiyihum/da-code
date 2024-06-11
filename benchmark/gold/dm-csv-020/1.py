import pandas as pd

df = pd.read_csv('../telco.csv')
df['Tenure in Years'] = pd.cut(x=df['Tenure in Months'], bins=range(0, 73, 12), labels=range(1, 7))
df[['Churn Category', 'Churn Reason']] = df[['Churn Category', 'Churn Reason']].fillna('not churned')
df[['Offer', 'Internet Type']] = df[['Offer', 'Internet Type']].fillna('None')

df_churn = df[df['Churn Label'] == 'Yes']

churn_by_zip = df_churn.groupby('Zip Code', as_index=False)['Churn Label'].count().rename(columns={'Churn Label': 'Churn'})

location_data = df[['Zip Code', 'City', 'Longitude', 'Latitude']].drop_duplicates()

df_map = pd.merge(location_data, churn_by_zip, on='Zip Code', how='left').fillna(0)

df_map_table = df_map.groupby('City', as_index=False)['Churn'].sum()

top_10_cities = df_map_table.sort_values(by='Churn', ascending=False).head(10).reset_index(drop=True)

top_10_cities.to_csv('top_10_cities.csv', index=False)
