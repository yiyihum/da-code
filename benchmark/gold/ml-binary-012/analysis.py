import pandas as pd
import re
import emoji
import spacy
import nltk
from nltk.stem import WordNetLemmatizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split

train_df = pd.read_csv("../training.1600000.processed.noemoticon.csv",encoding='latin-1', header=None)
test_df= pd.read_csv("../testdata.manual.2009.06.14.csv",header = None)
train_df.columns = ['Sentiment','Id', 'Time', 'Query','User', 'Text']
test_df.columns = ['Id', 'Time', 'Topic','User', 'Text']

nlp = spacy.load('en_core_web_sm')
def cleanNTokenize(df):
    #  Removing Emojis: 
    for col in df.columns:
        if col == 'text':
            df[col] = df[col].apply(lambda x: emoji.demojize(x))
    #  Replacing @ Tags with Empty Strings:
    pattern = r'@\w+'
    df['Text'] = df['Text'].apply(lambda x: re.sub(pattern, '', str(x)))
    #  Replacing # hashtags with Empty Strings: 
    pattern = r'#\w+'
    df['Text'] = df['Text'].apply(lambda x: re.sub(pattern, '', str(x)))
    #  Replacing Links with Empty Strings: 
    pattern = r'http\S+|www.\S+'
    df['Text'] = df['Text'].str.replace(pattern, '', regex=True)
    #  Removing all the stopwords:  
    stop_words = set(stopwords.words('english'))
    df['Text'] = df['Text'].apply(lambda x: ' '.join([word for word in word_tokenize(x) if word.lower() not in stop_words]))
    #  Convertin into LowerCase: 
    df['Text'] = df['Text'].str.lower()
    #  Removing Duplicates: 
    df.drop_duplicates(subset='Text', inplace=True)
    # Replacing punctuations with empty Strings: 
    df['Text'] = df['Text'].apply(lambda x: re.sub(r'[^\w\s]', '', x))
    # Finally Tokenizing
    df['tokenized'] = df['Text'].apply(word_tokenize) 
    return df

train_df = cleanNTokenize(train_df)
train_df.dropna(subset=['Text'], inplace=True)
train_df = train_df[train_df['Text'] != '']
test_df = cleanNTokenize(test_df)
# nltk.download()
nltk.download('wordnet')
# ls ../../root/nltk_data/corpora/wordnet.zip

def lemmatize_text(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]
    lemmatized_text = ' '.join(lemmatized_tokens)  # Join lemmatized tokens into a string
    return lemmatized_text

train_df['Lemmatized'] = train_df['tokenized'].apply(lemmatize_text)
test_df['Lemmatized'] = test_df['tokenized'].apply(lemmatize_text)
X = train_df['Lemmatized']
y = train_df['Sentiment']


X_train, X_val, y_train, y_val = train_test_split(X, y,
                                                    test_size =0.3, random_state = 0)
vectorizer = TfidfVectorizer()
X_train_transformed = vectorizer.fit_transform(X_train)

from sklearn.svm import LinearSVC
svm = LinearSVC()
svm.fit(X_train_transformed, y_train)

X_test = test_df['Lemmatized']
X_test_transformed = vectorizer.transform(X_test)
y_pred = svm.predict(X_test_transformed).tolist()

result = pd.DataFrame(data=y_pred.tolist(), columns=['emotion'])
result.to_csv('../sentiment.csv', index=False)





