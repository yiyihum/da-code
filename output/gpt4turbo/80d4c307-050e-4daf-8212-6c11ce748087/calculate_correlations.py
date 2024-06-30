import pandas as pd
import networkx as nx
from scipy.stats import pearsonr

# Function to calculate correlations and save to CSV
def calculate_correlations(book_number):
    # Read the book data
    df = pd.read_csv(f'book{book_number}.csv')
    
    # Create a graph from the dataframe
    G = nx.from_pandas_edgelist(df, 'Source', 'Target', ['weight'], create_using=nx.Graph())
    
    # Calculate centrality measures
    pagerank = nx.pagerank(G, weight='weight')
    betweenness = nx.betweenness_centrality(G, weight='weight')
    degree = dict(G.degree(weight='weight'))
    
    # Create dataframes from the centrality measures
    df_pagerank = pd.DataFrame(list(pagerank.items()), columns=['Character', 'PageRank'])
    df_betweenness = pd.DataFrame(list(betweenness.items()), columns=['Character', 'Betweenness'])
    df_degree = pd.DataFrame(list(degree.items()), columns=['Character', 'Degree'])
    
    # Merge the dataframes on the character names
    df_centrality = df_pagerank.merge(df_betweenness, on='Character').merge(df_degree, on='Character')
    
    # Calculate Pearson correlation coefficients
    pagerank_betweenness_corr = pearsonr(df_centrality['PageRank'], df_centrality['Betweenness'])[0]
    pagerank_degree_corr = pearsonr(df_centrality['PageRank'], df_centrality['Degree'])[0]
    betweenness_degree_corr = pearsonr(df_centrality['Betweenness'], df_centrality['Degree'])[0]
    
    # Create a correlation matrix
    correlation_matrix = pd.DataFrame({
        ' ': ['PageRank', 'Betweenness', 'Degree'],
        'PageRank': [1, pagerank_betweenness_corr, pagerank_degree_corr],
        'Betweenness': [pagerank_betweenness_corr, 1, betweenness_degree_corr],
        'Degree': [pagerank_degree_corr, betweenness_degree_corr, 1]
    })
    
    # Save the correlation matrix to a CSV file
    correlation_matrix.to_csv(f'correlation{book_number}.csv', index=False)

# Calculate correlations for books 3, 4, and 5
for book_number in range(3, 6):
    calculate_correlations(book_number)
