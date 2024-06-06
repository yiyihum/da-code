# Data manipulation and analysis
import numpy as np
import pandas as pd
from collections import Counter

# Visualization libraries
import matplotlib.pyplot as plt

# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('../synthetic_automobile_crash_data_india.csv')

# Bar plot of missing values count
plt.figure(figsize=(8, 6))
missing_values_count = df.isnull().sum()
missing_values_count = missing_values_count[missing_values_count > 0]
missing_values_count.sort_values(ascending=False).plot(kind='bar', color='skyblue')
plt.title('Feature Missing Values Count')
plt.xlabel('Features')
plt.ylabel('Missing Values Count')
plt.xticks(rotation=45)
plt.show()