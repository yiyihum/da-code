import pandas as pd

# Load the test data
test_df = pd.read_csv('/workspace/test.csv', names=['url'])

# Define a simple heuristic to classify URLs
def classify_url(url):
    if "phish" in url or "login" in url or "account" in url:
        return "phishing"
    elif "malware" in url or "virus" in url or "trojan" in url:
        return "malware"
    elif "deface" in url or "hack" in url:
        return "defacement"
    else:
        return "benign"

# Apply the heuristic to classify each URL
test_df['type'] = test_df['url'].apply(classify_url)

# Save the predictions to a new CSV file
test_df[['type']].to_csv('/workspace/type.csv', index=False)
