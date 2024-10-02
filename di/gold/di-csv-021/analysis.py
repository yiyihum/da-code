import pandas as pd


df = {
    "title": ["To and From New York", "Just Another Love Story", "Splatter", "Mad Ron's Prevues from Hell", "Even the Rain"],
    "country": ["United States", "Denmark", "United States", "United States", "Spain, Mexico, France"],
    "date_added": ["January 1, 2008", "May 5, 2009", "November 18, 2009", "November 1, 2010", "May 17, 2011"],
    "duration": ["81 min", "104 min", "29 min", "84 min", "103 min"]
}

df = pd.DataFrame(df)

df.to_csv("top_5_movies.csv", index=False)