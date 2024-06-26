import pandas as pd
import networkx as nx
from scipy.stats import pearsonr

# Function to calculate centrality measures and return them as a DataFrame
def calculate_centrality_measures(book_df):
    G = nx.from_pandas_edgelist(book_df, 'Source', 'Target', ['weight'], create_using=nx.Graph())
    pagerank = nx.pagerank(G, weight='weight')
    betweenness = nx.betweenness_centrality(G, weight='weight')
    degree = dict(G.degree(G.nodes(), weight='weight'))
    
    # Convert dictionaries to DataFrame
    centrality_df = pd.DataFrame({
        'PageRank': pd.Series(pagerank),
        'Betweenness': pd.Series(betweenness),
        'Degree': pd.Series(degree)
    })
    return centrality_df

# Read the book data and calculate centrality measures
books_data = {}
for i in range(1, 6):
    book_df = pd.read_csv(f'book{i}.csv')
    centrality_df = calculate_centrality_measures(book_df)
    books_data[f'book{i}'] = centrality_df

# Calculate Pearson correlation for each book and store results
correlation_results = {}
for book, df in books_data.items():
    pagerank_betweenness_corr, _ = pearsonr(df['PageRank'], df['Betweenness'])
    pagerank_degree_corr, _ = pearsonr(df['PageRank'], df['Degree'])
    betweenness_degree_corr, _ = pearsonr(df['Betweenness'], df['Degree'])
    correlation_results[book] = {
        'PageRank_Betweenness': pagerank_betweenness_corr,
        'PageRank_Degree': pagerank_degree_corr,
        'Betweenness_Degree': betweenness_degree_corr
    }

# Convert the results to a DataFrame and save to CSV
correlation_df = pd.DataFrame.from_dict(correlation_results, orient='index')
correlation_df.to_csv('/workspace/correlation_results.csv', index_label='Book')
print("Correlation calculations are complete.")
