import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns

df = pd.read_csv(r'../Electoral bond received by political parties.csv')
df = df.rename(columns={'Date of\rEncashment': 'Date_of\rEncashment', 'Name of the Political Party': 'Name_of_the_Political-Party'})
Political_party = df['Name_of_the_Political-Party'].unique()
for Political_partys in Political_party:
    print("->",Political_partys)
df['Denominations'] = df['Denominations'].str.replace(',', '')
df['Denominations'] = df['Denominations'].astype(int)
unique_parties = df['Name_of_the_Political-Party'].unique()
party_sums = {}
for party in unique_parties:
    party_sum = df[df['Name_of_the_Political-Party'] == party]['Denominations'].sum()
    party_sums[party] = party_sum


for party, total_denominations in party_sums.items():
    print(f"{party} Rec Electoral Bonds: {total_denominations}")

unique_parties = df['Name_of_the_Political-Party'].unique()
party_sums = {}

for party in unique_parties:
    party_sum = df[df['Name_of_the_Political-Party'] == party]['Denominations'].sum()
    party_sums[party] = party_sum

party_sums_df = pd.DataFrame(list(party_sums.items()), columns=['Party', 'Total_Denominations'])

import matplotlib.pyplot as plt

plt.figure(figsize=(14, 8))
plt.barh(party_sums_df['Party'], party_sums_df['Total_Denominations'], color='skyblue')
plt.xlabel('Total Denominations')
plt.ylabel('Political Party')
plt.title('Total Denominations by Political Party')

plt.tight_layout()
plt.savefig('party_sums_plot.png')
plt.show()
