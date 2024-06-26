import pandas as pd

# Initialize a dictionary to hold the protagonist for each book.
protagonists = {}

# Process each book file to find the protagonist.
for i in range(1, 6):
    # Read the book data.
    book_data = pd.read_csv(f'book{i}.csv')
    
    # Combine the Source and Target columns and count the cumulative weight for each character.
    character_weights = book_data.groupby('Source')['weight'].sum() + book_data.groupby('Target')['weight'].sum()
    
    # Find the character with the highest cumulative weight, which we assume to be the protagonist.
    protagonist = character_weights.idxmax()
    
    # Add the protagonist to the dictionary.
    protagonists[f'book{i}'] = protagonist

# Convert the dictionary to a DataFrame.
protagonists_df = pd.DataFrame(list(protagonists.items()), columns=['Book', 'Protagonist'])

# Save the DataFrame to a CSV file.
protagonists_df.to_csv('/workspace/result.csv', index=False)
