import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/netflix.csv')

# Group by 'genre' and get the title with the highest IMDb score in each genre
top_films = df.loc[df.groupby('genre')['imdb_score'].idxmax()]

# Plotting
plt.figure(figsize=(10, 8))
scatter = plt.scatter(top_films['title'], top_films['imdb_score'], c=top_films['genre'].astype('category').cat.codes, cmap='viridis')
plt.title('Top IMDb Score Films by Genre')
plt.xlabel('Title')
plt.ylabel('IMDb Score')
plt.xticks(rotation=90)
plt.colorbar(scatter, label='Genre')
plt.tight_layout()

# Save the plot
plt.savefig('/workspace/result.png')
