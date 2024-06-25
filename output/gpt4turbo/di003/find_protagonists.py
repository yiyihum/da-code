import pandas as pd

# Function to find the protagonist in a book
def find_protagonist(book_df):
    # Combine Source and Target into a single column and count the cumulative weight
    all_characters = pd.concat([book_df['Source'], book_df['Target']]).reset_index(drop=True)
    weights = pd.concat([book_df['weight'], book_df['weight']]).reset_index(drop=True)
    combined = pd.DataFrame({'Character': all_characters, 'Weight': weights})
    protagonist = combined.groupby('Character')['Weight'].sum().idxmax()
    return protagonist

# Read the CSV files and find the protagonist for each book
protagonists = {}
for i in range(1, 6):
    book_df = pd.read_csv(f'/workspace/book{i}.csv')
    protagonists[f'Book {i}'] = find_protagonist(book_df)

# Output the protagonists
print(protagonists)
