import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import warnings 
warnings.filterwarnings("ignore")
from catboost import Pool, CatBoostRegressor
from sklearn.metrics import mean_squared_error
from feature_engine.encoding import RareLabelEncoder

df_train = pd.read_csv('../top_10000_1960-now.csv').drop_duplicates()
df_test = pd.read_csv('../test.csv').drop_duplicates()
# select label
main_label = 'Popularity'
# exclude records with zero popularity
df_train = df_train[df_train[main_label]>0]

# extract song duration in minutes and group with larger bins
df_train['duration_minutes'] = df_train['Track Duration (ms)'].apply(lambda x: str(round(x/6e4)))
df_test['duration_minutes'] = df_test['Track Duration (ms)'].apply(lambda x: str(round(x/6e4)))
# extract song release year
df_train['release_year'] = df_train['Album Release Date'].fillna('None').apply(lambda x: x[:4])
df_test['release_year'] = df_test['Album Release Date'].fillna('None').apply(lambda x: x[:4])

# group columns to larger bins
for col in ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness', 'Speechiness', 'Valence']:
    df_train[col] = df_train[col].apply(lambda x: round(x,1))
    df_test[col] = df_test[col].apply(lambda x: round(x,1))

df_train['Loudness'] = df_train['Loudness'].apply(lambda x: 5*round(1/5*x))
df_test['Loudness'] = df_test['Loudness'].apply(lambda x: 5*round(1/5*x))
df_test['Tempo'] = df_test['Tempo'].apply(lambda x: 20*round(1/20*x))
# set up the rare label encoder limiting number of categories to max_n_categories
for col in ['Artist Name(s)', 'release_year', 'duration_minutes', 'Label']:
    df_train[col] = df_train[col].fillna('None')
    df_test[col] = df_test[col].fillna('None')
    encoder = RareLabelEncoder(n_categories=1, max_n_categories=70, replace_with='Other', tol=12/df_train.shape[0])
    df_train[col] = encoder.fit_transform(df_train[[col]])
    encoder = RareLabelEncoder(n_categories=1, max_n_categories=70, replace_with='Other', tol=12/df_test.shape[0])
    df_test[col] = encoder.fit_transform(df_test[[col]])


# drop unused columns
cols2drop = ['Track URI', 'Track Name', 'Artist URI(s)', 'Album URI', 'Album Name', 'ISRC', 'Track Number', 'Disc Number',
             'Album Artist URI(s)', 'Album Artist Name(s)', 'Album Image URL', 'Copyrights', 'Album Genres', 'Artist Genres',
             'Track Preview URL', 'Track Duration (ms)', 'Album Release Date', 'Label', 'Added By', 'Added At']
df_train = df_train.drop(cols2drop, axis=1)
df_test = df_test.drop(cols2drop, axis=1)

y_train = df_train[main_label].values.reshape(-1,)
X_train = df_train.drop([main_label], axis=1)
cat_cols = df_train.select_dtypes(include=['object']).columns
cat_cols_idx = [list(X_train.columns).index(c) for c in cat_cols]
X_test = df_test
y_test = []
# initialize Pool
train_pool = Pool(X_train, 
                  y_train, 
                  cat_features=cat_cols_idx)
# specify the training parameters 
model = CatBoostRegressor(iterations=300,
                          depth=6, 
                          learning_rate=0.07,
                          verbose=0,
                          loss_function='RMSE')
#train the model
model.fit(train_pool)
# make the prediction using the resulting model
y_pred = model.predict(X_test)

pred_df = pd.DataFrame(
    {
        "Popularity": y_pred.tolist()
    }
)

pred_df.to_csv('./popularity.csv', index=False)