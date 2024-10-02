import pandas as pd


df = {
    "title": ["The Magicians", "Henry Danger", "Bling Empire", "Disenchantment", "Carmen Sandiego"],
    "country": ["United States, Canada", "United States", "NaN", "United States", "United States"],
    "date_added": ["January 15, 2021", "January 15, 2021","January 15, 2021","January 15, 2021","January 15, 2021"],
    "duration": ["5 Seasons", "3 Seasons", "1 Seasons", "3 Seasons", "4 Seasons"]
}

df = pd.DataFrame(df)

df.to_csv("top_5_movies.csv", index=False)