import pandas as pd

# Load the dataset
movies_df = pd.read_csv('tmdb_5000_movies.csv')

# Check if the 'popularity' column exists
if 'popularity' in movies_df.columns:
    # Sort the movies by popularity in descending order and select the top 10
    top_movies = movies_df.nlargest(10, 'popularity')[['title', 'popularity']]
    
    # Save the result to a CSV file
    top_movies.to_csv('result.csv', index=False)
else:
    print("The 'popularity' column does not exist in the dataset.")
