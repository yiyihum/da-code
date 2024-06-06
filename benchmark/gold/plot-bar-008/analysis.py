import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

multiChoiceResp = pd.read_csv('../multipleChoiceResponses.csv')

country_df = multiChoiceResp['Q3'][1:].dropna()

index_to_drop = country_df.index[(country_df == 'Other') | (country_df == 'I do not wish to disclose my location')]
country_df = country_df.drop(index_to_drop)
country_df = country_df.replace(['United States of America', 'United Kingdom of Great Britain and Northern Ireland'], ['USA', 'UK & Northern Ireland'])

df = multiChoiceResp[['Q1', 'Q3']].dropna()

df = df.iloc[country_df.index]

top10_countries = ['United States of America', 'United Kingdom of Great Britain and Northern Ireland', 
                   'India', 'China', 'Russia', 'Brazil', 'Germany', 'France', 'Canada', 'Japan']

df = df[df['Q3'].isin(top10_countries)]
df['Q3'] = df['Q3'].replace(['United States of America', 'United Kingdom of Great Britain and Northern Ireland'], 
                            ['USA', 'UK & Northern Ireland'])
df['Q1'] = df['Q1'].replace(['Prefer not to say', 'Prefer to self-describe'], 'Others')

freq_df = df.groupby(['Q3'])['Q1'].value_counts().unstack().fillna(0)

pct_df = freq_df.divide(freq_df.sum(axis=1), axis=0) * 100

plt.figure(figsize=(16, 8))
bottom = np.zeros(len(pct_df))

for col in pct_df.columns:
    plt.bar(pct_df.index, pct_df[col], bottom=bottom, label=col)
    bottom += pct_df[col]

plt.title('Country-wise gender distribution')
plt.xlabel('Country')
plt.ylabel('Percentage')
plt.xticks(rotation=45)
plt.legend()

plt.savefig('./distribution.png', bbox_inches='tight')
