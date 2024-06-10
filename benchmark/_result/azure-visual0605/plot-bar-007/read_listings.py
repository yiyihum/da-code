import pandas as pd

# Load the listings.csv file
listings = pd.read_csv('/workspace/listings.csv')

# Count the number of listings in each neighborhood
neighborhood_counts = listings['neighbourhood'].value_counts()

# Select the top 10 neighborhoods with the highest number of listings
top_neighborhoods = neighborhood_counts.head(10)

# Save the top 10 neighborhoods and their counts to a CSV file
top_neighborhoods.to_csv('/workspace/top_neighborhoods.csv', header=True)
