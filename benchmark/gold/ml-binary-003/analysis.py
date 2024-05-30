import numpy as np 
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy, os
from sklearn.ensemble import RandomForestClassifier
from concurrent.futures import ProcessPoolExecutor

# Preprocessing The Data
nlp = spacy.load("en_core_web_sm")

def preprocess_data(text):
    tokens = nlp(str(text))
    filtered_tokens = [token.lemma_ for token in tokens if not token.is_punct and not token.is_stop]
    return " ".join(filtered_tokens)

def preprocess_data_chunk(chunk):
    return chunk.apply(preprocess_data)

def parallel_apply(data, func):
    with ProcessPoolExecutor() as executor:
        chunks = np.array_split(data, os.cpu_count())
        results = list(executor.map(func, chunks))
    return pd.concat(results, ignore_index=False)

if __name__ == '__main__':
    data = pd.read_csv("../twitter_training.csv")
    test_data = pd.read_csv('../twitter_validation.csv')
    map = {
        "Positive": 0,
        "Negative": 1,
        "Neutral": 2,
        "Irrelevant": 2
    }
    id2map ={
        "0": "Positive",
        "1": "Negative",
        "2": "Neutral"
    }

    data['preprocessed_data'] = parallel_apply(data['text'], preprocess_data_chunk)
    X = data['preprocessed_data']
    
    y = [map[label] for label in data['label']]

    v = TfidfVectorizer()
    X_train_normalized = v.fit_transform(X)

    rf_clf = RandomForestClassifier(n_estimators=60, n_jobs=-1)
    rf_clf.fit(X_train_normalized, y)

    test_data['preprocessed_data'] = test_data.text.apply(preprocess_data)
    x_test = test_data['preprocessed_data']
    x_testing = v.transform(x_test)
    y_pred = rf_clf.predict(x_testing)

    result = pd.DataFrame(
        {
            "result": [id2map[str(id)] for id in y_pred]
        }
    )
    
    result.to_csv('../prediction.csv', index=False)