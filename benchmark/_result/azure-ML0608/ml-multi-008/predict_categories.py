import pandas as pd

# Load the test data
test_df = pd.read_csv('/workspace/test.csv')

# Define keywords for each category
keywords = {
    'b': ['business', 'market', 'economy', 'finance', 'stock'],
    't': ['technology', 'tech', 'science', 'innovation', 'research'],
    'e': ['entertainment', 'movie', 'film', 'music', 'star', 'celebrity'],
    'm': ['health', 'medical', 'doctor', 'hospital', 'disease', 'patient']
}

# Function to predict category based on keywords
def predict_category(title):
    for category, keyword_list in keywords.items():
        if any(keyword in title.lower() for keyword in keyword_list):
            return category
    return 'b'  # Default to business if no keywords match

# Predict categories
test_df['CATEGORY'] = test_df['TITLE'].apply(predict_category)

# Save the predictions to a new CSV file
test_df[['CATEGORY']].to_csv('/workspace/category.csv', index=False)
