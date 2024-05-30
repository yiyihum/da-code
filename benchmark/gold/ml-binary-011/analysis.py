## Data Processing.
import pandas as pd
import numpy as np
## Machine Learning.
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
## Warning indication.
import warnings
warnings.filterwarnings('always') 

train = pd.read_csv("../Train.csv")
test = pd.read_csv("../Test.csv")
income_level = ['income_above_limit']
# The target column to be used for training 
target_column = train[income_level]
# Drop unique identifiers
Cols2drop = ['ID']
# Feature set corresponding to train and test data
train_df = train.drop(Cols2drop,axis=1)
test_id = test['ID']
test_df = test.drop(Cols2drop,axis=1)
# Encoding the target column and analyse the class structure.
target_column['income_above_limit'] = target_column['income_above_limit'].map({'Above limit':1,'Below limit':0})
def clean_strip(df):
    df = df.apply(lambda x : x.str.strip() if x.dtype == 'object' else x)
    df = df.replace('?', np.nan)
    return df

train_df = clean_strip(train_df)
test_df = clean_strip(test_df)
# Define a function that finds all columns with more than 70% NaN values and puts the names in a list.
nan_cols_drop  = []
for cols in test_df.columns:
    if test_df[cols].isna().sum()/test_df.shape[0] >0.7:
        nan_cols_drop.append(cols)
train_df = train_df.drop(nan_cols_drop,axis=1)
test_df  = test_df.drop(nan_cols_drop,axis=1)
def update_employment_related(df):
    df.loc[(df["age"] <= 18) & pd.isna(df["class"]), ["class", "occupation_code", "occupation_code_main"]] = ["Never worked", 0, "None"]
    df.loc[(df["age"] >= 65) & pd.isna(df["class"]), ["class", "occupation_code", "occupation_code_main"]] = ["Retired", 0, "None"]
    return df

## Apply the function to the DataFrame
train_df = update_employment_related(train_df.copy())  # Use a copy to avoid modifying the original
test_df = update_employment_related(test_df.copy())  # Use a copy to avoid modifying the original
def update_employment_related(df):
    df.loc[(df["occupation_code"] == 0) & pd.isna(df["class"]), ["class", "occupation_code", "occupation_code_main"]] = ["Unemployed", 0, "None"]
    return df

# Apply the function to the DataFrame
train_df = update_employment_related(train_df.copy())  # Use a copy to avoid modifying the original
test_df  = update_employment_related(test_df.copy())  # Use a copy to avoid modifying the original

# Have a look at the variables with missing values.
## Define a function that looks at the missing values and plots them in a bargraph.
def missing_values(df):
    na_columns_ = [col for col in df.columns if df[col].isnull().sum()>0]
    n_miss = df[na_columns_].isnull().sum().sort_values(ascending=False)
    ratio_ = (df[na_columns_].isnull().sum()/df.shape[0]*100).sort_values(ascending=False)
    missing_df = pd.concat([n_miss, np.round(ratio_,2)], axis=1,keys=["Missing values", "Ratio"])
    missing_df= pd.DataFrame(missing_df)

missing_values(train_df)
missing_values(test_df)

def impute_based_on_others(df):
    for col in df.columns:
        if df[col].dtype == "object":
            # For categorical variables:
            most_probable_values = df[col].dropna().mode().iloc[0]  # Get the most frequent value directly
            df[col].fillna(most_probable_values, inplace=True)  # Fill missing values efficiently
        else:
            # For numerical variables:
            imputer = SimpleImputer(strategy="most_frequent")
            df[col] = imputer.fit_transform(df[[col]])
    return df

## Apply the imputation function to the DataFrame
train_df = impute_based_on_others(train_df.copy())  # Use a copy to avoid modifying the original
test_df  = impute_based_on_others(test_df.copy())  # Use a copy to avoid modifying the original

# Gender & Income level encoding.
## Define a mapping dictionary with inclusive representation
gender_mapping = {
    "Male": 0,
    "Female": 1
}

income_mapping = {
    "Below limit": 0,
    "Above limit": 1
}

## Apply the mapping.
train_df['gender'] = train_df['gender'].map(gender_mapping)

test_df['gender'] = test_df['gender'].map(gender_mapping)

train_df['income_above_limit'] = train_df['income_above_limit'].map(income_mapping)

# Education level encoding.
## Create a list of all the unique values in the feature.
education_values = ['High school graduate', '5th or 6th grade',
                    'Bachelors degree(BA AB BS)', '9th grade', 'Children',
                    'Some college but no degree', '11th grade', '10th grade',
                    '7th and 8th grade', 'Associates degree-occup /vocational',
                    'Masters degree(MA MS MEng MEd MSW MBA)', '12th grade no diploma',
                    'Associates degree-academic program', 'Less than 1st grade',
                    'Prof school degree (MD DDS DVM LLB JD)',
                    '1st 2nd 3rd or 4th grade', 'Doctorate degree(PhD EdD)']

## Define the mapping rules
education_mapping = {"Children": "Below high school",
                    "1st 2nd 3rd or 4th grade": "Below high school",
                    "5th or 6th grade": "Below high school",
                    "7th and 8th grade": "Below high school",
                    "9th grade": "Below high school",
                    "10th grade": "Below high school",
                    "11th grade": "Below high school",
                    "12th grade no diploma": "Below high school",
                    "High school graduate": "High school",
                    "Some college but no degree": "Undergraduate",
                    "Associates degree-academic program": "Undergraduate",
                    "Associates degree-occup /vocational": "Undergraduate",
                    "Bachelors degree(BA AB BS)": "Undergraduate",
                    "Masters degree(MA MS MEng MEd MSW MBA)": "Postgraduate",
                    "Prof school degree (MD DDS DVM LLB JD)": "Postgraduate",
                    "Doctorate degree(PhD EdD)": "Postgraduate",
}

## Apply the mapping.
train_df['education'] = train_df['education'].map(education_mapping)
test_df['education'] = test_df['education'].map(education_mapping)

# Marital status encoding.
## Create a list of all the unique values in the feature.

marriage_status_values = ["Widowed", "Never married", "Married-civilian spouse present",
                        "Divorced", "Married-spouse absent","Separated","Married-A F spouse present"]

## Define the mapping rules.
marriage_mapping = {"Married-civilian spouse present": "Married",
                    "Married-spouse absent": "Married",
                    "Married-A F spouse present": "Married",
                    "Widowed": "Single", "Divorced": "Single",
                    "Separated": "Single", "Never married": "Single",
}

## Apply the mapping.
train_df['marital_status'] = train_df['marital_status'].map(marriage_mapping)
test_df['marital_status'] = test_df['marital_status'].map(marriage_mapping)

## Further map to binary values.
train_df["marital_status"] = train_df["marital_status"].map({"Married": 0, "Single": 1})
test_df['marital_status'] = test_df['marital_status'].map({"Married": 0, "Single": 1})

## Create a list of all the unique values in the feature.
citizenship_values = ["Native", "Foreign born- Not a citizen of U S", 
                    "Foreign born- U S citizen by naturalization",
                    "Native- Born abroad of American Parent(s)",
                    "Native- Born in Puerto Rico or U S Outlying",
]

## Define the mapping rules
citizenship_mapping = {"Native": "Citizen",
                    "Native- Born abroad of American Parent(s)": "Citizen",
                    "Native- Born in Puerto Rico or U S Outlying": "Citizen",
                    "Foreign born- U S citizen by naturalization": "Citizen",
                    "Foreign born- Not a citizen of U S": "Non-citizen"
}

## Apply the mapping.
train_df['citizenship'] = train_df['citizenship'].map(citizenship_mapping)
test_df['citizenship'] = test_df['citizenship'].map(citizenship_mapping)

## Further map to binary values.
train_df["citizenship"] = train_df["citizenship"].map({"Citizen": 0, "Non-citizen": 1})
test_df['citizenship'] = test_df['citizenship'].map({"Citizen": 0, "Non-citizen": 1})
# Hourly wage encoding.
## Define bin edges
bin_edges = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

## Create labels for the bins
bin_labels = ["0-1000", "1001-2000", "2001-3000", "3001-4000", "4001-5000",
            "5001-6000", "6001-7000", "7001-8000", "8001-9000", "9001-9999"]

## Apply the binning using pd.cut()
train_df["wage_per_hour"] = pd.cut(train_df["wage_per_hour"], bins=bin_edges, labels=bin_labels)
test_df["wage_per_hour"] = pd.cut(test_df["wage_per_hour"], bins=bin_edges, labels=bin_labels)
# Investment/capital market gains encoding.
## Define bin edges
bin_edges = [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]

## Create labels for the bins
bin_labels = ["0-10000", "10001-20000", "20001-30000", "30001-40000", "40001-50000",
            "50001-60000", "60001-70000", "70001-80000", "80001-90000", "90001-99999"]

## Apply the binning using pd.cut()
train_df["gains"] = pd.cut(train_df["gains"], bins=bin_edges, labels=bin_labels)
test_df["gains"] = pd.cut(test_df["gains"], bins=bin_edges, labels=bin_labels)
# Investment/capital market gains encoding.
## Define bin edges
bin_edges = [0, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]

## Create labels for the bins
bin_labels = ["0-10000", "10001-20000", "20001-30000", "30001-40000", "40001-50000",
            "50001-60000", "60001-70000", "70001-80000", "80001-90000", "90001-99999"]

## Apply the binning using pd.cut()
train_df["stocks_status"] = pd.cut(train_df["stocks_status"], bins=bin_edges, labels=bin_labels)
test_df["stocks_status"] = pd.cut(test_df["stocks_status"], bins=bin_edges, labels=bin_labels)
# Investment/capital market gains encoding.
## Define bin edges
bin_edges = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

## Create labels for the bins
bin_labels = ["0-1000", "1001-2000", "2001-3000", "3001-4000", "4001-5000",
            "5001-6000", "6001-7000", "7001-8000", "8001-9000", "9001-9999"]

## Apply the binning using pd.cut()
train_df["losses"] = pd.cut(train_df["losses"], bins=bin_edges, labels=bin_labels)
test_df["losses"] = pd.cut(test_df["losses"], bins=bin_edges, labels=bin_labels)
# Final Coding Procedure.

## Create a list of all the unique values in the feature
categorical_columns = ['class', 'race', 'education',
                    'is_hispanic', 'employment_commitment', 'working_week_per_year',
                    'industry_code_main', 'occupation_code_main', 'household_stat', 'stocks_status',
                    'household_summary', 'tax_status', 'citizenship', 'gains', 'losses',
                    'country_of_birth_own', 'country_of_birth_father', 'country_of_birth_mother',
                    'migration_code_change_in_msa', "wage_per_hour",
                    'migration_code_move_within_reg', 'migration_code_change_in_reg', 'residence_1_year_ago']

## Define function that codes the values into categorical codes

def consistent_coding(dataframes, categorical_columns):
    """Applies consistent category coding across multiple DataFrames."""

    # Create a dictionary to store global category mappings
    category_codes = {}

    for df in dataframes:
        for col in categorical_columns:
            if col not in category_codes:
                # Create mapping for new categories
                category_codes[col] = {
                    value: i for i, value in enumerate(df[col].dropna().unique())
                }

            # Apply mapping to DataFrame
            df[col] = df[col].astype('category')
            df[col] = df[col].cat.set_categories(list(category_codes[col].keys()))
            df[col] = df[col].cat.codes  # Assign codes based on global mapping
    
    df_category_codes = pd.DataFrame(category_codes)
    return dataframes
## Apply consistent coding to training & testing data.
consistent_coded_dfs = consistent_coding([train_df, test_df], categorical_columns)
train_df_coded, test_df_coded = consistent_coded_dfs  # Assign back to original DataFrames

# Separate features and target variable
X = train_df_coded.drop("income_above_limit", axis=1)
y = train_df_coded["income_above_limit"]

# Oversample minority class using SMOTE
smote = SMOTE(random_state=42)
X_train_oversampled, y_train_oversampled = smote.fit_resample(X, y)
X_train, y_train = X_train_oversampled, y_train_oversampled

# Create a Random Forest classifier with hyperparameter tuning
rf_clf_ov = RandomForestClassifier(n_estimators=100, random_state=42)  # Adjust hyperparameters as needed
rf_clf_ov.fit(X_train, y_train)

X_test = test_df_coded
# Make predictions on the testing set
y_pred = rf_clf_ov.predict(X_test)

result = pd.DataFrame(
    {
    'ID': test_id,
    'income_above_limit': y_pred
    }
)

result.to_csv("../results.csv", index=False)