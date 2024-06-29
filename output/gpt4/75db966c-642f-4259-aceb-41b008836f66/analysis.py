import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load the dataset
df = pd.read_csv('appstore_games.csv')

# Filter out games with user ratings less than 200 and update time less than 6 months
six_months_ago = datetime.now() - timedelta(days=6*30)
df['Current Version Release Date'] = pd.to_datetime(df['Current Version Release Date'], format='%d/%m/%Y', errors='coerce')
filtered_df = df[(df['User Rating Count'] >= 200) & 
                 (df['Current Version Release Date'] >= six_months_ago)]

# Categorize games into the four major genres
conditions = [
    filtered_df['Genres'].str.contains('Puzzle|Board', na=False),
    filtered_df['Genres'].str.contains('Action', na=False),
    filtered_df['Genres'].str.contains('Adventure|Role', na=False),
    filtered_df['Genres'].str.contains('Family|Education', na=False)
]
choices = ['Puzzle', 'Action', 'Adventure', 'Family']
filtered_df['Major Genre'] = np.select(conditions, choices, default='Other')

# Count the number of games for each of the four major genres
genre_counts = filtered_df['Major Genre'].value_counts()

# Plot their proportions in a pie chart
colors = ['Green', 'Orange', 'Blue', 'Red']
plt.figure(figsize=(12, 8))
plt.pie(genre_counts, labels=genre_counts.index, colors=colors, autopct='%1.1f%%')
plt.legend(genre_counts.index, title="Genres")
plt.title('Proportion of Games by Major Genre')
plt.savefig('result.png')
