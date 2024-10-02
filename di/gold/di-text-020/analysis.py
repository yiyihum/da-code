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
tossbat = Chennai[Chennai['toss_decision'] == 'bat']

tossfieldwin = Chennai[(Chennai['toss_decision'] == 'field') & (Chennai['winner'] == 'Chennai Super Kings')]
tossfieldlost = Chennai[(Chennai['toss_decision'] == 'field') & (Chennai['winner'] != 'Chennai Super Kings')]
tossbatwin = Chennai[(Chennai['toss_decision'] == 'bat') & (Chennai['winner'] == 'Chennai Super Kings')]

tossbatlost = Chennai[(Chennai['toss_decision'] == 'bat') & (Chennai['winner'] != 'Chennai Super Kings')]
total_matches = len(Chennai)
total_wins = len(Chennai[Chennai['winner'] == 'Chennai Super Kings'])

average_win = total_wins / total_matches

print("Average number of matches won by Chennai Super Kings  in Chennai:", average_win)
total_matches = len(Chennai)
total_losses = len(Chennai[Chennai['winner'] != 'Chennai Super Kings'])

average_loss = total_losses / total_matches

print("Average number of matches lost by Chennai Super Kings  in Chennai:", average_loss)
