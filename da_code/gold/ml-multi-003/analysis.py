import pandas as pd
import numpy as np
import time

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer # Create TD / TF-IDF Matricies
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression # Preform Logistic Regression
from sklearn.metrics import confusion_matrix # Make the Confustion Matrix
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score # for AUC, fpr, tpr, threshold and accuracy
from sklearn.metrics import precision_recall_fscore_support
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier

from nltk.corpus import stopwords # for the Stopwords list
from nltk.stem import PorterStemmer # for the porter Stemmer
import nltk # for other nltk functions
import re # for regular expression functions

from tqdm import tqdm  # for progress bar


# Read in data
job_postings = pd.read_csv("../postings.csv")
# Subsetting For Job Description and Experience Level
want =  ["description","formatted_experience_level"]
df = job_postings[want]
# Dropping Missing Values
df = df.dropna(subset=['formatted_experience_level']).reset_index(drop=True)
df['description'] = df['description'].astype(str)
df["formatted_experience_level"] = np.where(df["formatted_experience_level"] == 'Entry level',1,0)
def Features(df, column_name):
    feature_columns = ['word_cnt', 'sent_cnt', 'vocab_cnt', 'Avg_sent_word_cnt', 'lexical_richness','Readability_index']
    feature_data = []

    for index, row in df.iterrows():
        text = row[column_name]

        # Simple features (Word Count, Sentance Count, Vocabulary Count, Lexical Diversity)
        tokens = nltk.word_tokenize(text)
        char_cnt = len(tokens)

        words = [w for w in tokens if w.isalpha()]
        word_cnt = len(words)

        avg_word_length = char_cnt/word_cnt
        sents = nltk.sent_tokenize(text)
        sent_cnt = len(sents)
        avg_sent_length = word_cnt / sent_cnt if sent_cnt > 0 else 0
        avg_sent_length = round(avg_sent_length,2)
        vocab = set(words)
        vocab_cnt = len(vocab)
        lex_richness = round(vocab_cnt / word_cnt, 4)
        ARI = 4.71*avg_word_length + .5*avg_sent_length - 21.43
        # Append the column data
        feature_data.append([word_cnt, sent_cnt, vocab_cnt, avg_sent_length, lex_richness ,ARI]) # dropped avg_sent_length
    feature_df = pd.DataFrame(feature_data, columns=feature_columns)
    # Combine the original DataFrame with the new DataFrame containing features
    result_df = pd.concat([df, feature_df], axis=1)
    return result_df
FE_df = Features(df,'description')
FE_df['Cust_Service'] = FE_df['description'].apply(lambda x: 1 if 'customer service' in x.lower() else 0)
FE_df['diploma_ged'] = FE_df['description'].apply(lambda x: 1 if 'diploma ged' in x.lower() else 0)
FE_df['per_hour'] = FE_df['description'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
FE_df['diploma_equiv'] = FE_df['description'].apply(lambda x: 1 if 'diploma equivalent' in x.lower() else 0)
FE_df['project_management'] = FE_df['description'].apply(lambda x: 1 if 'project management' in x.lower() else 0)
FE_df['cross_functional'] = FE_df['description'].apply(lambda x: 1 if 'cross functional' in x.lower() else 0)
FE_df['minimum_years'] = FE_df['description'].apply(lambda x: 1 if 'minimum years' in x.lower() else 0)
FE_df['experience_working'] = FE_df['description'].apply(lambda x: 1 if 'experience working' in x.lower() else 0)
FE_df['management'] = FE_df['description'].apply(lambda x: 1 if 'management ' in x.lower() else 0)
FE_df['track_record'] = FE_df['description'].apply(lambda x: 1 if 'track_record ' in x.lower() else 0)
x_fe = FE_df.drop(['description', 'formatted_experience_level'], axis=1)
y_fe = FE_df['formatted_experience_level']
X_train2, X_test2, y_train2, y_test2 = train_test_split(x_fe, y_fe, test_size = 0.2, random_state = 1)
from imblearn.over_sampling import RandomOverSampler
ros = RandomOverSampler(random_state=42)
X_train_resampled, y_train_resampled = ros.fit_resample(X_train2, y_train2)
scaler = MinMaxScaler()
X_train_resampled_normalized = scaler.fit_transform(X_train_resampled)
X_test2_normalized = scaler.transform(X_test2)

X_train_resampled_normalized = pd.DataFrame(X_train_resampled_normalized, columns=X_train2.columns)
X_test2_normalized = pd.DataFrame(X_test2_normalized, columns=X_test2.columns)
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

stop_words = set(stopwords.words('english'))
#stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def preprocess(text):
    tokens = nltk.word_tokenize(text)
    text = [word.lower() for word in tokens if word.isalpha()]
    text = [word for word in text if word not in stop_words]
    text = [lemmatizer.lemmatize(word) for word in text] # Stemms the word (Porter in this case)
    return ' '.join(text)
X = df.iloc[:,:-1]
y = df.iloc[:,-1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)
# Preprocess the training and testing sets for X and Y
X_train = [preprocess(desc) for desc in X_train.description]
X_test = [preprocess(desc) for desc in X_test.description]
vectorizer = CountVectorizer()
X_train_td = vectorizer.fit_transform(X_train)
# Vectorization of text data
tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)
print("Shape of X_train_vect: ", X_train_tfidf.shape)
print("Shape of X_test_vect: ", X_test_tfidf.shape)
from imblearn.over_sampling import RandomOverSampler
ros = RandomOverSampler(random_state=42)
X_train_resampled_td, y_train_resampled = ros.fit_resample(X_train_tfidf, y_train)
X_train_resampled_tfidf, y_train_resampled = ros.fit_resample(X_train_tfidf, y_train)
from sklearn.ensemble import GradientBoostingClassifier
def objective(trial):
    param_dist = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 20),
        }

    gbm_td = GradientBoostingClassifier(random_state=42, **param_dist)
    cv_scores = cross_val_score(gbm_td, X_train_resampled_td, y_train_resampled, cv=3, n_jobs = -1)

    return cv_scores.mean()

