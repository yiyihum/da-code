import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

data = pd.read_csv('../athlete_events.csv')
regions = pd.read_csv('../noc_regions.csv')

merged = pd.merge(data, regions, on='NOC', how='left')
goldMedals = merged[(merged.Medal == 'Gold')]
goldMedals = goldMedals[np.isfinite(goldMedals['Age'])]

masterDisciplines = goldMedals['Sport'][goldMedals['Age'] > 50]
totalGoldMedals = goldMedals.region.value_counts().reset_index(name='Medal').head(5)
print(totalGoldMedals)
