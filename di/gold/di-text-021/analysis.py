import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import folium
from scipy.stats import ttest_ind
from scipy.stats import zscore

restaurants = pd.read_csv("../North America Restaurants.csv")
restaurants.head(5)

restaurants.columns
null_cuisine = restaurants[restaurants['cuisines'].isnull()]

restaurants = restaurants.drop(null_cuisine.index)

restaurant_counts = restaurants.groupby(['city', 'state']).size().reset_index(name='restaurant_count')
max_concentration = restaurant_counts.loc[restaurant_counts['restaurant_count'].idxmax()]

print("City with the highest concentration of restaurants:")
print("City:", max_concentration['city'])
print("State:", max_concentration['state'])
print("Number of Restaurants:", max_concentration['restaurant_count'])
