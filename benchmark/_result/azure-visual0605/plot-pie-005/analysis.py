import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load the dataset
df = pd.read_csv('appstore_games.csv')

# Filter out games with user ratings less than 200
df = df[df['User Rating Count'] >= 200]

# Convert 'Current Version Release Date' to datetime without filtering to check the correct format
df['Current Version Release Date'] = pd.to_datetime(df['Current Version Release Date'], format='%d/%m/%Y', errors='coerce')

# Categorize games based on the rules provided
def categorize_genre(genres):
    if 'Puzzle' in genres or 'Board' in genres:
        return 'Puzzle'
    elif 'Action' in genres:
        return 'Action'
    elif 'Adventure' in genres or 'Role' in genres:
        return 'Adventure'
    elif 'Family' in genres or 'Education' in genres:
        return 'Family'
    else:
        return 'Other'

# Use .loc to avoid SettingWithCopyWarning
df.loc[:, 'Major Genre'] = df['Genres'].apply(lambda x: categorize_genre(x.split(', ')))

# Check if the expected genres are present in the data
expected_genres = ['Puzzle', 'Action', 'Adventure', 'Family']
genre_counts = df['Major Genre'].value_counts()
genre_counts = genre_counts[genre_counts.index.isin(expected_genres)]

# If no expected genres are present, print a message and exit
if genre_counts.empty:
    print("No games found for the expected genres after filtering.")
    exit()

# Plot their proportions in a pie chart
colors = ['Green', 'Orange', 'Blue', 'Red']
plt.figure(figsize=(12, 8))
plt.pie(genre_counts, labels=genre_counts.index, colors=colors, autopct='%1.1f%%')
plt.legend(genre_counts.index)
plt.title('Proportions of Games by Major Genre')
plt.savefig('result.png')
