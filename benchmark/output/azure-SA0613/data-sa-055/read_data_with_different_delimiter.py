import pandas as pd

# Attempt to read the CSV file with a different delimiter
try:
    df = pd.read_csv('frog_tongue.csv', delimiter=',')
    print(df.head())
except pd.errors.ParserError as e:
    print("ParserError:", e)
    # If the delimiter is not a comma, try a tab delimiter
    try:
        df = pd.read_csv('frog_tongue.csv', delimiter='\t')
        print(df.head())
    except pd.errors.ParserError as e:
        print("ParserError with tab delimiter:", e)
