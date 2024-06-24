import pandas as pd

# Loading data
credits = pd.read_csv('/Users/stewiepeter/Desktop/VsProjects/VaftBench/kaggleNo.4/tmdb_5000_credits.csv')
movies = pd.read_csv('/Users/stewiepeter/Desktop/VsProjects/VaftBench/kaggleNo.4/tmdb_5000_movies.csv')

# Merging movies and credits datasets based on the movie ID to combine movie details
data = pd.merge(movies, credits, left_on = 'id', right_on = 'movie_id')

# Function to calculate weighted rating of each movie
def weightedRating(row, m, C):
    # Extracting the number of votes (v) and the average rating (R) from the row
    v = row['vote_count']
    R = row['vote_average']
    
    # Calculating the weighted rating and rounding it upto 3 decimal places
    return round((v * R + m * C) / (v + m), 3)

# Function to get top-rated movies by genre and verdict (if given)
def getTopRatedMovies(data, genre = None, verdict = None, percentile = 0.85):
    # Filtering data by genre if specified
    if genre:
        data = data[data['genres'].apply(lambda x : genre.replace(' ', '').lower() in x)]
    # Filtering data by verdict if specified
    if verdict:
        data = data[data['verdict'] == verdict.replace(' ', '').lower()]
    # Calculating the mean vote average across the filtered dataset
    C = data['vote_average'].mean()
    # Calculating the given percentile of the vote count (default 85th)
    m = data['vote_count'].quantile(percentile)
    # Filtering the dataset to select only those movies with a vote count greater than or equal to the calculated minimum votes (m)
    topMovies = data.loc[data['vote_count'] >= m].copy()
    # Calculating weighted rating for each movie
    topMovies['score'] = topMovies.apply(weightedRating, args = (m, C), axis = 1)
    # Sorting the dataframe based on the calculated scores in descending order to get the top-rated movies
    topMovies = topMovies.sort_values('score', ascending = False)
    # Returning the recommended movies
    return topMovies['original_title'][:10].reset_index(drop=True)

# Getting top-rated movies without specifying a genre or verdict
results = getTopRatedMovies(data)

with open(r'./result.txt', 'w') as r:
    for movie in results:
        r.write(str(movie))
        r.write('\n')
