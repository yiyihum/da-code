import pandas as pd

df = pd.read_csv('../train.csv')

df.drop(['ID_LAT_LON_YEAR_WEEK', 'emission'], axis=1, inplace=True)

missing_rows = df[df.isnull().all(axis=1)]

print(missing_rows)

