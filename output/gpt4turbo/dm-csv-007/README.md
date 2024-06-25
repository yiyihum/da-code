## About Dataset

### Background

The dataset explores the potential success of a movie before its release by analyzing various factors such as plot, cast, crew, budget, and revenues of several thousand films. The objective is to understand if certain companies, like Pixar, have a consistent formula for success and to predict which films will be highly rated regardless of their commercial success.

### Data Source Transfer Summary

The original version of this dataset has been replaced with a similar set of films and data fields from The Movie Database (TMDb) due to a DMCA takedown request from IMDB. The new dataset contains full credits for both cast and crew, actor and actresses listed in order of appearance, and more current revenue figures.

### Data Source Transfer Details

- Some new columns contain JSON.
- Fields like runtime may vary between versions.
- A separate file now contains full credits for cast and crew.
- Data fields are user-filled and may not agree on keywords, genres, ratings, etc.
- Existing kernels will render normally until re-run.

New columns include:

- homepage
- id
- original_title
- overview
- popularity
- production_companies
- production_countries
- release_date
- spoken_languages
- status
- tagline
- vote_average

Lost columns include:

- actor_1_facebook_likes
- actor_2_facebook_likes
- actor_3_facebook_likes
- aspect_ratio
- cast_total_facebook_likes
- color
- content_rating
- director_facebook_likes
- facenumber_in_poster
- movie_facebook_likes
- movie_imdb_link
- num_critic_for_reviews
- num_user_for_reviews
