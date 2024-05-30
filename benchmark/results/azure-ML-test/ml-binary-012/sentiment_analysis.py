import csv

# Define some simple positive and negative keywords for heuristic analysis
positive_keywords = ['love', 'loved', 'like', 'good', 'great', 'happy', 'fantastic', 'cool']
negative_keywords = ['hate', 'bad', 'sad', 'terrible', 'awful', 'worse', 'worst']

def classify_sentiment(text):
    # Simple heuristic: if any positive keyword is in the text, return 'positive'
    for word in positive_keywords:
        if word in text.lower():
            return 'positive'
    # If any negative keyword is in the text, return 'negative'
    for word in negative_keywords:
        if word in text.lower():
            return 'negative'
    # If neither, return 'neutral'
    return 'neutral'

def main():
    input_filename = 'testdata.manual.2009.06.14.csv'
    output_filename = 'sentiment.csv'

    with open(input_filename, 'r', newline='', encoding='ISO-8859-1') as csvfile:
        reader = csv.reader(csvfile)
        with open(output_filename, 'w', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(['emotion'])  # Write header

            for row in reader:
                # Add error handling for rows with an unexpected number of fields
                if len(row) < 6:
                    continue  # Skip rows that do not have the expected number of fields

                tweet_text = row[5]
                sentiment = classify_sentiment(tweet_text)
                writer.writerow([sentiment])

if __name__ == '__main__':
    main()