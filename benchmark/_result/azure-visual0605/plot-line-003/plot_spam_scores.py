import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('/workspace/fake.csv')

# Convert the 'published' and 'crawled' columns to datetime with utc=True
df['published'] = pd.to_datetime(df['published'], errors='coerce', utc=True)
df['crawled'] = pd.to_datetime(df['crawled'], errors='coerce', utc=True)

# Drop rows where 'published' or 'crawled' could not be converted to datetime
df = df.dropna(subset=['published', 'crawled'])

# Extract the day from the 'published' and 'crawled' datetime objects
df['published_day'] = df['published'].dt.date
df['crawled_day'] = df['crawled'].dt.date

# Group by the day and calculate the average spam score for each day
published_spam_scores = df.groupby('published_day')['spam_score'].mean().reset_index()
crawled_spam_scores = df.groupby('crawled_day')['spam_score'].mean().reset_index()

# Plotting
plt.figure(figsize=(30, 7))

# Plot the average spam score for each published day
plt.plot(published_spam_scores['published_day'], published_spam_scores['spam_score'], label='Published')

# Plot the average spam score for each crawled day
plt.plot(crawled_spam_scores['crawled_day'], crawled_spam_scores['spam_score'], label='Crawled')

# Labeling the axes
plt.xlabel('Day')
plt.ylabel('Spam Score')

# Adding a legend
plt.legend()

# Save the plot as 'output.png'
plt.savefig('/workspace/output.png')
