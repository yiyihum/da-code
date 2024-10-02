# importing  required libraries
import pandas as pd
import numpy as np
# for visualization
import seaborn as sns
import matplotlib.pyplot as plt
# import warings
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('../world-data-2023.csv')
# total columns
for count,coulumn_name in enumerate(df.keys(),1):
    print(count,coulumn_name)
# numerical columns
numerical_column = df.select_dtypes(include=['float']).columns
print(f'We have total {len(numerical_column)} these floating columns:') 
for count,column_name in enumerate(df.select_dtypes(include=['float']).columns,1):
    print(f'\t\t\t\t{count}) {column_name}')
columns_to_convert = ['Density\n(P/Km2)', 'Agricultural Land( %)', 'Land Area(Km2)',
                      'Birth Rate', 'Co2-Emissions', 'Forested Area (%)',
                      'CPI', 'CPI Change (%)', 'Fertility Rate', 'Gasoline Price', 'GDP',
                      'Gross primary education enrollment (%)', 'Armed Forces size',
                      'Gross tertiary education enrollment (%)', 'Infant mortality',
                      'Life expectancy', 'Maternal mortality ratio', 'Minimum wage', 
                      'Out of pocket health expenditure', 'Physicians per thousand', 
                      'Population', 'Population: Labor force participation (%)', 
                      'Tax revenue (%)', 'Total tax rate', 'Unemployment rate', 'Urban_population']
df[columns_to_convert] = df[columns_to_convert].applymap(lambda x: float(str(x).replace('%','').replace(',', '').replace('$','')))
# our dataset is in good condtion we inpute numerical columns with mean and categorical columns with mode

# Imputing of Numerical Columns
df['Density\n(P/Km2)'].fillna(df['Density\n(P/Km2)'].mean,inplace=True)
df['Tax revenue (%)'].fillna(df['Tax revenue (%)'].mean(),inplace=True)
df['Armed Forces size'].fillna(df['Armed Forces size'].mean(),inplace=True)
df['Gasoline Price'].fillna(df['Gasoline Price'].mean(),inplace=True)
df['Minimum wage'].fillna(df['Minimum wage'].mean(),inplace=True)
df['Population'].fillna(df['Population'].mean(),inplace=True)
df['Population: Labor force participation (%)'].fillna(df['Population: Labor force participation (%)'].mean(),inplace=True)
df['Unemployment rate'].fillna(df['Unemployment rate'].mean(),inplace=True)
df['CPI'].fillna(df['CPI'].mean(),inplace=True) 
df['CPI Change (%)'].fillna(df['CPI Change (%)'].mean(),inplace=True)
df['Maternal mortality ratio'].fillna(df['Maternal mortality ratio'].mean(),inplace=True)
df['Gross tertiary education enrollment (%)'].fillna(df['Gross tertiary education enrollment (%)'].mean(), inplace=True)
df['Total tax rate'].fillna(df['Total tax rate'].mean(), inplace=True)
df['Life expectancy'].fillna(df['Life expectancy'].mean(),inplace=True)
df['Physicians per thousand'].fillna(df['Physicians per thousand'].mean(),inplace=True)
df['Out of pocket health expenditure'].fillna(df['Out of pocket health expenditure'].mean(),inplace=True)
df['Gross primary education enrollment (%)'].fillna(df['Gross primary education enrollment (%)'].mean(),inplace=True)
df['Fertility Rate'].fillna(df['Fertility Rate'].mean(),inplace=True)
df['Co2-Emissions'].fillna(df['Co2-Emissions'].mean(),inplace=True)
df['Agricultural Land( %)'].fillna(df['Agricultural Land( %)'].mean(),inplace=True)
df['Forested Area (%)'].fillna(df['Forested Area (%)'].mean(),inplace=True)
df['Infant mortality'].fillna(df['Infant mortality'].mean(),inplace=True)
df['Birth Rate'].fillna(df['Birth Rate'].mean(),inplace=True)
df['Urban_population'].fillna(df['Urban_population'].mean(),inplace=True)
df['Longitude'].fillna(df['Longitude'].mean(),inplace=True)
df['Calling Code'].fillna(df['Calling Code'].mean(),inplace=True)
df['Land Area(Km2)'].fillna(df['Land Area(Km2)'].mean(),inplace=True)
df['GDP'].fillna(df['GDP'].mean(),inplace=True)
df['Latitude'].fillna(df['Latitude'].mean(),inplace=True)

# Imputing of Categorical Columns
df['Abbreviation'].fillna(df['Abbreviation'].mode()[0],inplace=True)
df['Capital/Major City'].fillna(df['Capital/Major City'].mode()[0], inplace=True)
df['Currency-Code'].fillna(df['Currency-Code'].mode()[0], inplace=True)
df['Largest city'].fillna(df['Largest city'].mode()[0],inplace=True)
df['Official language'].fillna(df['Official language'].mode()[0],inplace=True)

sorrted = df.sort_values(by=['Agricultural Land( %)'],ascending=False)
top_countries = sorrted.head(10)[['Country','Agricultural Land( %)']]
# print result
print('Top Agricultral Countries:\n\n',top_countries)
