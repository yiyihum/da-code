import pandas as pd
import numpy as np
import seaborn as sns                       
import matplotlib.pyplot as plt             

def impute_end_date(kdrama_copy, start_date_col='Start_date', day_aired_col='Day_aired', episodes_col='Episodes'):
    """
    Imputes missing End_date values in a kdrama DataFrame based on the provided Start_date, Day_aired, and Episodes information.
    """
    # Convert Start_date to a datetime object and format it
    kdrama_copy[start_date_col] = pd.to_datetime(kdrama_copy[start_date_col]).dt.strftime('%d/%m/%Y')

    # Split the Day_aired string into individual days
    kdrama_copy[day_aired_col] = kdrama_copy[day_aired_col].str.split(', ')

    # Iterate over the rows of the DataFrame and impute missing End_date values
    for i, row in kdrama_copy[kdrama_copy['End_date'].isnull()].iterrows():
        days_aired = row[day_aired_col]

        # Check if the show airs once or twice a week
        if len(days_aired) == 1:
            # Impute missing end_date values based on the assumption that the show airs once a week on the same day
            kdrama_copy.at[i, 'End_date'] = (pd.to_datetime(row[start_date_col], format='%d/%m/%Y')
                                         + pd.DateOffset(days=7*(row[episodes_col]-1))).normalize().strftime('%d/%m/%Y')

        elif len(days_aired) == 2:
            # Impute missing end_date values based on the assumption that the show airs twice a week on the same days
            kdrama_copy.at[i, 'End_date'] = (pd.to_datetime(row[start_date_col], format='%d/%m/%Y')
                                         + pd.DateOffset(days=6*(row[episodes_col]-2))).strftime('%d/%m/%Y')

        else:
            # Handle the case where there are more than 2 days of airing per week
            print(f"Error: Can't handle more than 2 days of airing per week for kdrama {row['Title']}")

    # Format the End_date column
    kdrama_copy['End_date'] = pd.to_datetime(kdrama_copy['End_date']).dt.strftime('%d/%m/%Y')

    return kdrama_copy

kdrama = pd.read_csv('../top100_kdrama.csv')
kdrama.head()

kdrama.isna().sum()
kdrama_copy = kdrama.copy()

imputed_kdrama = impute_end_date(kdrama_copy)
imputed_kdrama.head()
# Counting individual genre
from collections import Counter

genres_list = []
for genres in imputed_kdrama['Genre'].to_list():
    genres = genres.strip().split(", ")
    for genres in genres:
        genres_list.append(genres)
        
genres_df = pd.DataFrame.from_dict(Counter(genres_list),orient='index').rename(columns={0:'Count'})
genres_df.sort_values(by='Count',ascending = False,inplace = True)
genres_df.head()



