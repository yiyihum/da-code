import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import os
print(os.listdir("../"))

data = pd.read_csv('../athlete_events.csv')
regions = pd.read_csv('../noc_regions.csv')

merged = pd.merge(data, regions, on='NOC', how='left')
goldMedals = merged[(merged.Medal == 'Gold')]
goldMedals.head()
goldMedals.isnull().any()

womenInOlympics = merged[(merged.Sex == 'F') & (merged.Season == 'Summer')]
womenInOlympics.head(10)
womenInOlympics.loc[womenInOlympics['Year'] == 1900].head(10)

print(womenInOlympics['ID'].loc[womenInOlympics['Year'] == 1900].count())