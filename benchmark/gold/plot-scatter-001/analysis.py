import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../netflix.csv')
# Create an in-memory SQLite database
conn = sqlite3.connect(':memory:')

# Convert the DataFrame to an SQLite table
df.to_sql('netflix', conn, index=False)

# Create a cursor object
cursor = conn.cursor()

query = """
SELECT
    genre,
    language,
    COUNT(*) AS title_count
FROM netflix
GROUP BY genre, language
ORDER BY genre, title_count DESC;
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)

query = """
SELECT 
    genre,
    title,
    imdb_score
FROM netflix AS n1
WHERE imdb_score = (
    SELECT MAX(imdb_score)
    FROM netflix AS n2
    WHERE n1.genre = n2.genre
);
"""

cursor.execute(query)

rows = cursor.fetchall()

for row in rows:
    print(row)

df = pd.DataFrame(rows, columns=['Genre', 'Title', 'IMDb_Score'])


plt.figure(figsize=(30, 20))
sns.scatterplot(data=df, x='Title', y='IMDb_Score', hue='Genre', palette='viridis')

plt.title('IMDb Score vs Genre')
plt.xlabel('Title')
plt.ylabel('IMDb Score')
plt.xticks(rotation=90)

handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles, labels, title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()
