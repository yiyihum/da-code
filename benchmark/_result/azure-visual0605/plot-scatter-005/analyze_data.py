import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Load the data
df = pd.read_csv('/workspace/steam.csv')

# Standardize the Average Playtime and Positive Ratings
df['average_playtime_std'] = (df['average_playtime'] - df['average_playtime'].mean()) / df['average_playtime'].std()
df['positive_ratings_std'] = (df['positive_ratings'] - df['positive_ratings'].mean()) / df['positive_ratings'].std()

# Calculate the Pearson correlation coefficient
correlation, _ = pearsonr(df['average_playtime_std'], df['positive_ratings_std'])

# Create a scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df['average_playtime_std'], df['positive_ratings_std'], alpha=0.5)
plt.title('Correlation Between Average Playtime and Positive Ratings')
plt.xlabel('Average Playtime (Standardized)')
plt.ylabel('Positive Ratings (Standardized)')
plt.grid(True)
plt.savefig('/workspace/result.png')

# Output the Pearson correlation coefficient
print(f'Pearson correlation coefficient: {correlation}')
