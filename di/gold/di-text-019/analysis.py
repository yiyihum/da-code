import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

matchdata = pd.read_csv('../match_data.csv')
matchinfodata = pd.read_csv('../match_info_data.csv')

Chennai = matchinfodata[matchinfodata['city'] == 'Chennai']
Chennaiwin = Chennai[Chennai['winner'] == 'Chennai Super Kings']
Chennaiwincount = len(Chennaiwin)
Chennailost = Chennai[Chennai['winner'] != 'Chennai Super Kings']
Chennailostcount = len(Chennailost)

tossfield = Chennai[Chennai['toss_decision'] == 'field']
tossfieldcount = len(tossfield)
tossbat = Chennai[Chennai['toss_decision'] == 'bat']
tossfieldwin = Chennai[(Chennai['toss_decision'] == 'field') & (Chennai['winner'] == 'Chennai Super Kings')]
tossfieldlost = Chennai[(Chennai['toss_decision'] == 'field') & (Chennai['winner'] != 'Chennai Super Kings')]

tossbatwin = Chennai[(Chennai['toss_decision'] == 'bat') & (Chennai['winner'] == 'Chennai Super Kings')]
tossbatlost = Chennai[(Chennai['toss_decision'] == 'bat') & (Chennai['winner'] != 'Chennai Super Kings')]
unique_cities = matchinfodata['city'].unique()
print("List of all cities:", unique_cities)
city_match_count = matchinfodata['city'].value_counts().reset_index()
city_match_count.columns = ['City', 'Total Matches']

print("Total Matches played in each city:")
print(city_match_count)

Mumbai = matchinfodata[matchinfodata['city'] == 'Mumbai']
Mumbaiwin = Mumbai[Mumbai['winner'] == 'Chennai Super Kings']

Mumbailost = Mumbai[Mumbai['winner'] != 'Chennai Super Kings']

Mumbaiwincount = len(Mumbaiwin)
Mumbailostcount = len(Mumbailost)
print("Chennai Super Kings Wins in Mumbai Stadium:", Mumbaiwincount)
print("Chennai Super Kings Losses in Mumbai Stadium:", Mumbailostcount)
