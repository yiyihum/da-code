import numpy as np 
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

true_data = pd.read_csv('../True.csv')
fake_data = pd.read_csv('../Fake.csv')
validation_data = pd.read_csv('../validation.csv')

all_data=pd.concat([fake_data, true_data])
random_permutation = np.random.permutation(len(all_data))
all_data= all_data.iloc[random_permutation]
filterd_data=all_data.loc[:, ['title', 'text', "subject", 'label']]
filterd_data['training_feature']=filterd_data['title']+' '+filterd_data['text']+' '+filterd_data['subject']
validation_data=validation_data.loc[:, ['title', 'text', "subject"]]
validation_data['training_feature'] = validation_data['title'] + ' ' + validation_data['text'] + ' '+ validation_data['subject']

X_train= filterd_data['training_feature'].values
y_train = filterd_data['label']

X_val = validation_data['training_feature'].values

vectorizer= TfidfVectorizer()
X_train=vectorizer.fit_transform(X_train)
x_val = vectorizer.transform(X_val)

model=LogisticRegression()
model.fit(X_train,y_train)

y_pred = model.predict(x_val)

df = pd.DataFrame(data=y_pred, columns=['result'])

df.to_csv('../result.csv', index=False)