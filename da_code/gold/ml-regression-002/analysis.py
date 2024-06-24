import numpy as np
import pandas as pd
# Model Creation
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from category_encoders import OrdinalEncoder

# Warnings Ignore
import warnings
warnings.filterwarnings("ignore")

df = pd.read_csv('../energy_dataset.csv')
correlations = df.corr(method='pearson')
#print(correlations['price actual'].sort_values(ascending=False).to_string())

# Assign Variable to drop columns
zero_val_cols = ['generation marine',
                 'generation geothermal',
                 'generation fossil peat',
                 'generation wind offshore',
                 'generation fossil oil shale',
                 'forecast wind offshore eday ahead',
                 'generation fossil coal-derived gas',
                 'generation hydro pumped storage aggregated']

# Drop Columns with zero values
heat_map_features = df.drop(columns=zero_val_cols,axis=1)

def wrangle(filepath):    
    # Read in the data, parse dates, and set the index
    df = pd.read_csv(filepath,parse_dates=['time'],index_col='time')
    # Rename columns by replacing all - or blank space with _
    df.columns = df.columns.str.replace(' ','_').str.replace('-','_')
    # Make the index DT
    df.index = pd.to_datetime(df.index, utc=True)    

    # Drop all columns with data leakage, or 90% + null
    df.drop(columns=['price_day_ahead',
                     'generation_marine',
                     'total_load_forecast',
                     'generation_geothermal',
                     'generation_fossil_peat',
                     'generation_wind_offshore',
                     'forecast_solar_day_ahead',
                     'generation_fossil_oil_shale',
                     'forecast_wind_onshore_day_ahead',
                     'forecast_wind_offshore_eday_ahead',
                     'generation_fossil_coal_derived_gas',
                     'generation_hydro_pumped_storage_aggregated'],inplace=True)
    
    # Drop Outlier row 2014 for plotting
    try:
        df = df.drop(pd.Timestamp('2014-12-31 23:00:00+00:00'))
    except:
        pass 
    
    # Sort index
    df = df.sort_index()
    
    # Set conditional satements for filtering times of month to season value
    condition_winter = (df.index.month>=1)&(df.index.month<=3)
    condtion_spring = (df.index.month>=4)&(df.index.month<=6)
    condition_summer = (df.index.month>=7)&(df.index.month<=9)
    condition_automn = (df.index.month>=10)@(df.index.month<=12)
    
    # Create column in dataframe that inputs the season based on the conditions created above
    df['season'] = np.where(condition_winter,'winter',
                            np.where(condtion_spring,'spring',
                                     np.where(condition_summer,'summer',
                                              np.where(condition_automn,'automn',np.nan))))

    return df

# Applying the wrangle function to the dataset
df=wrangle('../energy_dataset.csv')
test_df=wrangle('../test.csv')

# Create Target variable
target='price_actual'
# Split data into feature matrix and target vector
y_train,X_train=df[target],df.drop(columns=target)
X_test = test_df.iloc[:, :]


# Ordinal Encoder to transform Seasons column
ordinal = OrdinalEncoder()
ordinal_fit = ordinal.fit(X_train)
XT_train = ordinal.transform(X_train)
XT_test = ordinal.transform(X_test)

# Simple imputer to fill nan values, then transform sets
simp = SimpleImputer(strategy='mean')
simp_fit = simp.fit(XT_train)
XT_train = simp.transform(XT_train)
XT_test = simp.transform(XT_test)

# Assigning model variables
model_rfr = RandomForestRegressor()
# Fitting models
model_rfr.fit(XT_train,y_train);
y_pred = model_rfr.predict(XT_test)

pred_df = pd.DataFrame(
    {
        "price actual": y_pred.tolist()
    }
)
pred_df.to_csv('../result.csv', index=False)