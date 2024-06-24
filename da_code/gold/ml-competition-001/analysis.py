# import libraries
# 1. to handle the data
import pandas as pd
import numpy as np
# To preprocess the data
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
# machine learning
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
#Model
import lightgbm as lgb
from catboost import CatBoostClassifier, Pool
from catboost.utils import eval_metric
#Evaluation
from sklearn.metrics import roc_auc_score
# ignore warnings   
import warnings
warnings.filterwarnings('ignore')

# Load Submission Data 
df_submission = pd.read_csv('../sample_submission.csv')
# Load test Data 
df_test = pd.read_csv('../test.csv')
# Load Train Dataset and show head of Data 
#Train Data 
df_train = pd.read_csv('../train.csv')

# making a Copy of the Test Data for Future Use 
df_test = pd.read_csv('../test.csv')
df_test_ov = df_test.copy()
print(df_test.head())
print(df_train.head())

# Checking the number of rows and columns
num_train_rows, num_train_columns = df_train.shape
num_test_rows, num_test_columns = df_test.shape
num_submission_rows, num_submission_columns = df_submission.shape
print("Training Data:")
print(f"Number of Rows: {num_train_rows}")
print(f"Number of Columns: {num_train_columns}\n")
print("Test Data:")
print(f"Number of Rows: {num_test_rows}")
print(f"Number of Columns: {num_test_columns}\n")
print("Submission Data:")
print(f"Number of Rows: {num_submission_rows}")
print(f"Number of Columns: {num_submission_columns}")

# Null Values in Train 
train_null = df_train.isnull().sum().sum()
#Null Count in Test 
test_null = df_test.isnull().sum().sum()
#null Count in Submission
submission_null = df_submission.isnull().sum().sum()
print(f'Null Count in Train: {train_null}')
print(f'Null Count in Test: {test_null}')
print(f'Null Count in Submission: {submission_null}')

# Count duplicate rows in train_data
train_duplicates = df_train.duplicated().sum()
# Count duplicate rows in test_data
test_duplicates = df_test.duplicated().sum()
# Count duplicate rows in original_data
submission_duplicates = df_submission.duplicated().sum()
# Print the results
print(f"Number of duplicate rows in train_data: {train_duplicates}")
print(f"Number of duplicate rows in test_data: {test_duplicates}")
print(f"Number of duplicate rows in test_data: {submission_duplicates}")

# Null Values in Train 
train_null = df_train.isnull().sum().sum()
print(f'Null Count in Train: {train_null}')
# Count duplicate rows in train_data
train_duplicates = df_train.duplicated().sum()
# Print the results
print(f"Number of duplicate rows in train_data: {train_duplicates}")

# Load Train Dataset and show head of Data 
#Train Data 
df_train = pd.read_csv('../train.csv')
df_train.head()

numeirc_cols = ['Age','CreditScore', 'Balance','EstimatedSalary']
#Use Loop Function
for col in numeirc_cols:
    sc = MinMaxScaler()
    df_train[col+"_scaled"] = sc.fit_transform(df_train[[col]])
    df_test[col+"_scaled"] = sc.fit_transform(df_test[[col]])

# Combining Customerid , Surname , Geography , and Gender , Estimated Slaray  and Making New Column in both Data Frames 
df_train['Sur_Geo_Gend_Sal'] = df_train['CustomerId'].astype('str')+df_train['Surname']+df_train['Geography']+df_train['Gender']+np.round(df_train.EstimatedSalary).astype('str')
df_test['Sur_Geo_Gend_Sal'] = df_test['CustomerId'].astype('str')+df_test['Surname']+df_test['Geography']+df_test['Gender']+np.round(df_test.EstimatedSalary).astype('str')

def get_vectors(df_train,df_test,col_name):

    vectorizer = TfidfVectorizer(max_features=1000)
    vectors_train = vectorizer.fit_transform(df_train[col_name])
    vectors_test = vectorizer.transform(df_test[col_name])
    
    #Dimensionality Reduction Using SVD ( Singular Value Decompostion)
    svd = TruncatedSVD(3)
    x_sv_train = svd.fit_transform(vectors_train)
    x_sv_test = svd.transform(vectors_test)

    # Convert to DataFrames
    tfidf_df_train = pd.DataFrame(x_sv_train)
    tfidf_df_test = pd.DataFrame(x_sv_test)

    # Naming columns in the new DataFrames
    cols = [(col_name + "_tfidf_" + str(f)) for f in tfidf_df_train.columns.to_list()]
    tfidf_df_train.columns = cols
    tfidf_df_test.columns = cols

    # Reset the index of the DataFrames before concatenation
    df_train = df_train.reset_index(drop=True)
    df_test = df_test.reset_index(drop=True)

    # Concatenate transformed features with original data
    df_train = pd.concat([df_train, tfidf_df_train], axis="columns")
    df_test = pd.concat([df_test, tfidf_df_test], axis="columns")
    return df_train,df_test

df_train,df_test = get_vectors(df_train,df_test,'Surname')
df_train,df_test = get_vectors(df_train,df_test,'Sur_Geo_Gend_Sal')

def feature_data(df):
    
    df['Senior'] = df['Age'].apply(lambda x: 1 if x >= 60 else 0)
    df['Active_by_CreditCard'] = df['HasCrCard'] * df['IsActiveMember']
    df['Products_Per_Tenure'] =  df['Tenure'] / df['NumOfProducts']
    df['AgeCat'] = np.round(df.Age/20).astype('int').astype('category')
    
    cat_cols = ['Geography', 'Gender', 'NumOfProducts','AgeCat']
    #onehotEncoding
    df=pd.get_dummies(df,columns=cat_cols)
    return df

#Genrating New Features
df_train = feature_data(df_train)
df_test = feature_data(df_test)

##Selecting Columns FOr use 
feat_cols=df_train.columns.drop(['id', 'CustomerId', 'Surname','Exited','Sur_Geo_Gend_Sal'])
feat_cols=feat_cols.drop(numeirc_cols)

#Printing
print(feat_cols)
df_train.head()

X=df_train[feat_cols]
y=df_train['Exited']

# Features to use
feat_cols = X.columns

#Intilize folds 
n = 5

#Cat_features
cat_features = np.where(X.dtypes != np.float64)[0]

# Initialize StratifiedKFold
folds = StratifiedKFold(n_splits=n, random_state=42, shuffle=True)
test_preds = np.empty((n, len(df_test)))
auc_vals_cat = []

# Loop through folds 
for n_fold, (train_idx, valid_idx) in enumerate(folds.split(X, y)):
    ''' in each iteration of the cross-validation loop, the model is trained on a specific subset 
    of the data (training set) and validated on a different subset (validation set), facilitating the evaluation of the model's performance 
    across diverse portions of the dataset.'''
    X_train_fold, y_train_fold = X.iloc[train_idx], y.iloc[train_idx]
    X_test_fold, y_test_fold = X.iloc[valid_idx], y.iloc[valid_idx]
    
    train_pool = Pool(X_train_fold, y_train_fold,cat_features=cat_features)
    val_pool = Pool(X_test_fold, y_test_fold,cat_features=cat_features)
    
    cat_model = CatBoostClassifier(
    eval_metric='AUC',
    learning_rate=0.022,
    iterations=1000)
    cat_model.fit(train_pool, eval_set=val_pool,verbose=False)
    
    #Predicting Prohabilites 
    y_pred_val_cat = cat_model.predict_proba(X_test_fold[feat_cols])[:,1]
    auc_val = roc_auc_score(y_test_fold, y_pred_val_cat)
    print("AUC for fold ",n_fold,": ",auc_val)
    auc_vals_cat.append(auc_val)
    
    y_pred_test_cat = cat_model.predict_proba(df_test[feat_cols])[:,1]
    test_preds[n_fold, :] = y_pred_test_cat
    print(f"------- Loop Completed for Fold {n_fold} --------")

y_pred_cat = test_preds.mean(axis=0)
# making a Copy of the Test Data for Future Use 
df_test = pd.read_csv('../test.csv')
df_test_ov = df_test.copy()
#Importing the Orginal Dataset 
df_orig=pd.read_csv("../Churn_Modelling.csv")
#Extracting the Column name From the Original Dataset
orig_cols=list(df_orig.columns.drop(['RowNumber','Exited']))
# Renaming the Column Exited With Exited_Orig in the Original Dataset
df_orig.rename(columns={'Exited':'Exited_Orig'},inplace=True)
# Here the Tricky part , Reversing the Label , Example Where [Exited is 1 , we replace it with 0] and Where Exited is 0 we replace it with 1.
df_orig['Exited_Orig']=df_orig['Exited_Orig'].map({0:1,1:0})
# Now we are Merging The Original Dataset And Testing Dataset It performs a left join based on specified columns (orig_cols)
# and selects specific columns of interest. The resulting DataFrame includes the original exit status ('Exited_Orig') for corresponding
# 'id' values, and missing values are filled with -1.
df_test_merg=df_test_ov.merge(df_orig,on=orig_cols,how='left')[['id','Exited_Orig']].fillna(-1)
# Creating a Submission Dataframe
df_sub = df_test_merg[['id','Exited_Orig']]
#Creating a New Column Named Exited , np.where Updates  If the 'Exited_Orig' column has a value of -1, it replaces it 
#with the predicted values (y_pred). If 'Exited_Orig' is not -1, it keeps the original values from 'Exited_Orig'
df_sub['Exited'] = np.where(df_sub.Exited_Orig==-1,y_pred_cat,df_sub.Exited_Orig)
# Drooping The Exited_orig Column
df_sub.drop('Exited_Orig',axis=1,inplace=True)
#Head Of Submission Data 
df_sub.head()
df_sub.to_csv("submission.csv",index=False)
print("Submission file created successfully!")