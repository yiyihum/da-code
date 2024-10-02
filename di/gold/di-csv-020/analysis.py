# Importing libraries
import pandas as pd
import os
from warnings import filterwarnings
filterwarnings('ignore')
import matplotlib.pyplot as plt
import seaborn as sns

# Defining directory variables
DATA_PATH = '../'
FILENAME = 'netflix_titles.csv'

# Reading the csv file
df = pd.read_csv(os.path.join(DATA_PATH, FILENAME))
print(f'The dataset has {df.shape[0]} rows and {df.shape[1]} columns')
df.head()

