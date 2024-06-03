import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import (
    AdaBoostClassifier,
    RandomForestClassifier
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from mlxtend.classifier import StackingClassifier

train_data=pd.read_csv("../train.csv")
test_data=pd.read_csv("../test.csv")

train_data.drop(columns={"CustomerID"},inplace=True)
test_data.drop(columns={"CustomerID"},inplace=True)
#Finding Categorical  Columns
cat_col=[]
for col  in test_data.columns:
    if(test_data[col].dtypes=='object'):
        cat_col.append(col)
#Finding Numerical Columns
num_col=[]
for col in test_data.columns:
    if(test_data[col].dtypes!='object'):
        num_col.append(col)

# Data Cleaning & Preprocessing
train_data.isnull().mean()*100
test_data.isnull().mean()*100
from sklearn.preprocessing import LabelEncoder
SubscriptionType_encoder=LabelEncoder()
train_data['SubscriptionType']=SubscriptionType_encoder.fit_transform(train_data['SubscriptionType'])
PaymentMethod_encoder=LabelEncoder()
train_data['PaymentMethod']=PaymentMethod_encoder.fit_transform(train_data['PaymentMethod'])
PaperlessBilling_encoder=LabelEncoder()
train_data['PaperlessBilling']=PaperlessBilling_encoder.fit_transform(train_data['PaperlessBilling'])
ContentType_encoder=LabelEncoder()
train_data['ContentType']=ContentType_encoder.fit_transform(train_data['ContentType'])
MultiDeviceAccess_encoder=LabelEncoder()
train_data['MultiDeviceAccess']=MultiDeviceAccess_encoder.fit_transform(train_data['MultiDeviceAccess'])
DeviceRegistered_encoder=LabelEncoder()
train_data['DeviceRegistered']=DeviceRegistered_encoder.fit_transform(train_data['DeviceRegistered'])
GenrePreference_encoder=LabelEncoder()
train_data['GenrePreference']=GenrePreference_encoder.fit_transform(train_data['GenrePreference'])
Gender_encoder=LabelEncoder()
train_data['Gender']=Gender_encoder.fit_transform(train_data['Gender'])
ParentalControl_encoder=LabelEncoder()
train_data['ParentalControl']=ParentalControl_encoder.fit_transform(train_data['ParentalControl'])
SubtitlesEnabled_encoder=LabelEncoder()
train_data['SubtitlesEnabled']=SubtitlesEnabled_encoder.fit_transform(train_data['SubtitlesEnabled'])
#SubscriptionType
test_data['SubscriptionType']=SubscriptionType_encoder.transform(test_data['SubscriptionType'])
#PaymentMethod
test_data['PaymentMethod']=PaymentMethod_encoder.transform(test_data['PaymentMethod'])
#PaperlessBilling
test_data['PaperlessBilling']=PaperlessBilling_encoder.transform(test_data['PaperlessBilling'])
#ContentType
test_data['ContentType']=ContentType_encoder.transform(test_data['ContentType'])
#MultiDeviceAccess
test_data['MultiDeviceAccess']=MultiDeviceAccess_encoder.transform(test_data['MultiDeviceAccess'])
#DeviceRegistered
test_data['DeviceRegistered']=DeviceRegistered_encoder.transform(test_data['DeviceRegistered'])
#GenrePreference
test_data['GenrePreference']=GenrePreference_encoder.transform(test_data['GenrePreference'])
#Gender
test_data['Gender']=Gender_encoder.transform(test_data['Gender'])
#ParentalControl
test_data['ParentalControl']=ParentalControl_encoder.transform(test_data['ParentalControl'])
#SubtitlesEnabled
test_data['SubtitlesEnabled']=SubtitlesEnabled_encoder.transform(test_data['SubtitlesEnabled'])
from sklearn.preprocessing import StandardScaler
#AccountAge
AccountAge_scaler=StandardScaler()
train_data['AccountAge']=AccountAge_scaler.fit_transform(np.array(train_data['AccountAge']).reshape(len(train_data['AccountAge']),1))
#MonthlyCharges
MonthlyCharges_scaler=StandardScaler()
train_data['MonthlyCharges']=MonthlyCharges_scaler.fit_transform(np.array(train_data['MonthlyCharges']).reshape(len(train_data['MonthlyCharges']),1))
#TotalCharges
TotalCharges_scaler=StandardScaler()
train_data['TotalCharges']=TotalCharges_scaler.fit_transform(np.array(train_data['TotalCharges']).reshape(len(train_data['TotalCharges']),1))
#ViewingHoursPerWeek
ViewingHoursPerWeek_scaler=StandardScaler()
train_data['ViewingHoursPerWeek']=ViewingHoursPerWeek_scaler.fit_transform(np.array(train_data['ViewingHoursPerWeek']).reshape(len(train_data['ViewingHoursPerWeek']),1))
#AverageViewingDuration
AverageViewingDuration_scaler=StandardScaler()
train_data['AverageViewingDuration']=AverageViewingDuration_scaler.fit_transform(np.array(train_data['AverageViewingDuration']).reshape(len(train_data['AverageViewingDuration']),1))
#ContentDownloadsPerMonth
ContentDownloadsPerMonth_scaler=StandardScaler()
train_data['ContentDownloadsPerMonth']=ContentDownloadsPerMonth_scaler.fit_transform(np.array(train_data['ContentDownloadsPerMonth']).reshape(len(train_data['ContentDownloadsPerMonth']),1))
#UserRating
UserRating_scaler=StandardScaler()
train_data['UserRating']=UserRating_scaler.fit_transform(np.array(train_data['UserRating']).reshape(len(train_data['UserRating']),1))
#SupportTicketsPerMonth
SupportTicketsPerMonth_scaler=StandardScaler()
train_data['SupportTicketsPerMonth']=SupportTicketsPerMonth_scaler.fit_transform(np.array(train_data['SupportTicketsPerMonth']).reshape(len(train_data['SupportTicketsPerMonth']),1))
#WatchlistSize
WatchlistSize_scaler=StandardScaler()
train_data['WatchlistSize']=WatchlistSize_scaler.fit_transform(np.array(train_data['WatchlistSize']).reshape(len(train_data['WatchlistSize']),1))
#AccountAge
test_data['AccountAge']=AccountAge_scaler.transform(np.array(test_data['AccountAge']).reshape(len(test_data['AccountAge']),1))
#MonthlyCharges
test_data['MonthlyCharges']=MonthlyCharges_scaler.transform(np.array(test_data['MonthlyCharges']).reshape(len(test_data['MonthlyCharges']),1))
#TotalCharges
test_data['TotalCharges']=TotalCharges_scaler.transform(np.array(test_data['TotalCharges']).reshape(len(test_data['TotalCharges']),1))
#ViewingHoursPerWeek
test_data['ViewingHoursPerWeek']=ViewingHoursPerWeek_scaler.transform(np.array(test_data['ViewingHoursPerWeek']).reshape(len(test_data['ViewingHoursPerWeek']),1))
#AverageViewingDuration
test_data['AverageViewingDuration']=AverageViewingDuration_scaler.transform(np.array(test_data['AverageViewingDuration']).reshape(len(test_data['AverageViewingDuration']),1))
#ContentDownloadsPerMonth
test_data['ContentDownloadsPerMonth']=ContentDownloadsPerMonth_scaler.transform(np.array(test_data['ContentDownloadsPerMonth']).reshape(len(test_data['ContentDownloadsPerMonth']),1))
#UserRating
test_data['UserRating']=UserRating_scaler.transform(np.array(test_data['UserRating']).reshape(len(test_data['UserRating']),1))
#SupportTicketsPerMonth
test_data['SupportTicketsPerMonth']=SupportTicketsPerMonth_scaler.transform(np.array(test_data['SupportTicketsPerMonth']).reshape(len(test_data['SupportTicketsPerMonth']),1))
#WatchlistSize
test_data['WatchlistSize']=WatchlistSize_scaler.transform(np.array(test_data['WatchlistSize']).reshape(len(test_data['WatchlistSize']),1))
# Feature and Target
Feature=train_data.drop(columns="Churn")
Target=train_data['Churn']

smote = SMOTE(random_state=42)
Feature,Target = smote.fit_resample(Feature,Target)

model= AdaBoostClassifier(estimator=RandomForestClassifier(n_jobs=-1),
                                learning_rate=1e-3,
                                algorithm='SAMME',
                                random_state=42
                                )

#Model Training
model.fit(Feature[['AccountAge', 'MonthlyCharges', 'TotalCharges', 'SubscriptionType', 'PaymentMethod', 'PaperlessBilling', 'ContentType', 'MultiDeviceAccess', 'DeviceRegistered', 'ViewingHoursPerWeek', 'AverageViewingDuration', 'ContentDownloadsPerMonth', 'GenrePreference', 'UserRating', 'SupportTicketsPerMonth', 'Gender', 'WatchlistSize', 'ParentalControl', 'SubtitlesEnabled']],Target)
#Model Testing
y_pred=model.predict(test_data[['AccountAge', 'MonthlyCharges', 'TotalCharges', 'SubscriptionType', 'PaymentMethod', 'PaperlessBilling', 'ContentType', 'MultiDeviceAccess', 'DeviceRegistered', 'ViewingHoursPerWeek', 'AverageViewingDuration', 'ContentDownloadsPerMonth', 'GenrePreference', 'UserRating', 'SupportTicketsPerMonth', 'Gender', 'WatchlistSize', 'ParentalControl', 'SubtitlesEnabled']])

result = pd.DataFrame(data=y_pred.tolist(), columns=['Churn'])

result.to_csv('../churn.csv', index=False)