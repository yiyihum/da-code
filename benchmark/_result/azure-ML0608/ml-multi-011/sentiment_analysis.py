import csv
from textblob import TextBlob

def classify_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

def predict_sentiments(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile,          open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=['Sentiment'])
        writer.writeheader()
        
        for row in reader:
            tweet = row['OriginalTweet']
            sentiment = classify_sentiment(tweet)
            writer.writerow({'Sentiment': sentiment})

predict_sentiments('Corona_NLP_test.csv', 'sentiment.csv')
