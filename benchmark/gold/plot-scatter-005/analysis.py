import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

steam_df = pd.read_csv('../steam.csv') 

def calculate_middle_owner(owners_str):
    lower, upper = map(int, owners_str.split("-"))
    return (upper - lower) / 2

steam_df['middle_owners'] = steam_df['owners'].apply(calculate_middle_owner)

# Split and expand the 'platforms' column into separate platforms
steam_df['platforms'] = steam_df['platforms'].str.split(';')

from scipy.stats import pearsonr

# Filter for games with positive ratings and playtime
data = steam_df[(steam_df['positive_ratings'] > 0) & (steam_df['average_playtime'] > 0)] 

# Standardize columns
data['average_playtime_std'] = (data['average_playtime'] - data['average_playtime'].mean()) / data['average_playtime'].std() 
data['positive_ratings_std'] = (data['positive_ratings'] - data['positive_ratings'].mean()) / data['positive_ratings'].std()

# Calculate Pearson correlation
corr, p = pearsonr(data['average_playtime_std'], data['positive_ratings_std'])
print('Correlation:', corr)

# Create scatter plot 
plt.figure(figsize=(10,6))
sns.scatterplot(data=data, x='average_playtime_std', y='positive_ratings_std', alpha=0.5)

# Label axes
plt.xlabel('Average Playtime (Standardized)')  
plt.ylabel('Positive Ratings (Standardized)')
plt.title('Correlation Between Average Playtime and Positive Ratings')

plt.savefig('result.png')