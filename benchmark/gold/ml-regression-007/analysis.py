import numpy as np  # Import NumPy for handling numerical operations
import pandas as pd  # Import Pandas for data manipulation and analysis
import warnings  # Import Warnings to suppress unnecessary warnings

# Suppress warning messages
warnings.filterwarnings("ignore")

# Import CatBoostRegressor for building a regression model
from catboost import Pool, CatBoostRegressor

# Import train_test_split for splitting the data into training and testing sets
from sklearn.model_selection import train_test_split

df = pd.read_csv('../data.csv')  # Reads the dataset from a CSV file into a Pandas DataFrame
test = pd.read_csv('../test.csv')
item0 = df.shape[0]  # Stores the initial number of rows in the DataFrame
df = df.drop_duplicates()  # Removes duplicate rows from the DataFrame
item1 = df.shape[0]  # Stores the number of rows after removing duplicates
print(f"There are {item0-item1} duplicates found in the dataset")  # Prints the number of duplicates that were removed

# Select only specific columns of interest
selected_cols = ['AVG_JOB_SATISFACTION', 'AVG_WEEKLY_WORKING_HOURS', 
       'MEDIAN_NET_INCOME', 'GENDER_PAY_GAP', 'INABILITY_UNEXPECTED_EXPENSES',
       'WORKING_HOME', 'USUALLY_WORKING_EVENING', 'USUALLY_WORKING_SUNDAYS',
       'USUALLY_WORKING_SATURDAYS', 'FINANTIAL_SITUATION_RATING',
       'LONG_WORKING_HOURS']
df = df[selected_cols]
test = test[selected_cols[1:]]

# log10_transform 'reviews' and group to larger bins
def log10_group_bin(x):
    try:
        return str(round(1/5*round(5*np.log10(1+x)) ,1) )
    except:
        return 'None'
    
main_label = 'AVG_JOB_SATISFACTION'
# Function to bin numerical columns into equal quantile-based bins
def bin_column(df, col_name, num_bins=3):
    # Calculate the bin edges to evenly split the numerical column
    bin_edges = pd.qcut(df[col_name], q=num_bins, retbins=True)[1]

    # Define labels for the categorical bins based on bin edges
    bin_labels = [f'{int(bin_edges[i])}-{int(bin_edges[i+1])}' for i in range(num_bins)]

    # Use pd.qcut to create quantile-based bins with an equal number of records in each bin
    df[col_name] = pd.qcut(df[col_name], q=num_bins, labels=False)

    # Update the bin labels to be more descriptive
    df[col_name] = df[col_name].map(lambda x: bin_labels[x])

    # Convert the column to object dtype
    df[col_name] = df[col_name].astype('object')

    return df

# Iterate through DataFrame columns (excluding the main label column)
for col in df.columns:
    if col != main_label:
        try:
            # Bin the column if it's numerical
            df = bin_column(df, col)
            test = bin_column(test, col)
            print(f"Binned column {col}")
        except:
            df[f'log10_{col}'] = df[col].apply(log10_group_bin)
            df = df.drop([col], axis=1)
            test[f'log10_{col}'] = test[col].apply(log10_group_bin)
            test = test.drop([col], axis=1)

y = df[main_label].values.reshape(-1,)

# Create the feature matrix 'X' by dropping the 'main_label' column from the DataFrame 'df'
X = df.drop([main_label], axis=1)

# Identify categorical columns in the DataFrame 'df'
# These columns contain non-numeric data
cat_cols = df.select_dtypes(include=['object']).columns

# Create a list of indices for categorical columns in the feature matrix 'X'
cat_cols_idx = [list(X.columns).index(c) for c in cat_cols]

# Split the data into training and testing sets
# - 'X_train' and 'y_train' will contain the training features and labels, respectively
# - 'X_test' and 'y_test' will contain the testing features and labels, respectively
# The split is done with a 50% test size, a random seed of 0, and stratification based on the selected column(s)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0, stratify=df[['FINANTIAL_SITUATION_RATING']])

X_train = X
y_train = y
X_test = test
train_pool = Pool(X_train, 
                  y_train, 
                  cat_features=cat_cols_idx)  # Create a training data pool with categorical features

# Specify the training parameters for the CatBoostRegressor model
model = CatBoostRegressor(iterations=500,    # Number of boosting iterations
                          depth=5,           # Maximum depth of trees in the ensemble
                          verbose=0,         # Set verbosity level to 0 (no output during training)
                          early_stopping_rounds=50, # Early stopping rounds
                          learning_rate=0.06,  # Learning rate for gradient boosting
                          loss_function='RMSE')  # Loss function to optimize (Root Mean Squared Error)

# Train the CatBoostRegressor model on the training data
model.fit(train_pool)

# Make predictions using the trained model on both the training and testing data
y_pred = model.predict(X_test)    # Predictions on the testing data


y_test = pd.read_csv('./job_satisfaction.csv')['AVG_JOB_SATISFACTION'].tolist()

from sklearn import metrics
print('MAE:', round(metrics.mean_absolute_error(y_test, y_pred),3))  
print('MSE:', round(metrics.mean_squared_error(y_test, y_pred),3))  
print('RMSE:', round(np.sqrt(metrics.mean_squared_error(y_test, y_pred)),3))
print('R2_score:', round(metrics.r2_score(y_test, y_pred),6))
print('RMSLE:', round(np.log(np.sqrt(metrics.mean_squared_error(y_test, y_pred))),3))
