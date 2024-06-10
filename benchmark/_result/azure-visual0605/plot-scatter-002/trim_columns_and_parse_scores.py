import pandas as pd
import matplotlib.pyplot as plt

# Read the compressed CSV file
df = pd.read_csv('/workspace/odds_series_matches.csv.gz', compression='gzip', encoding='latin1')

# Trim whitespace from column names
df.columns = df.columns.str.strip()

# Parse the 'detailed_score' column to extract fulltime home and away scores
df[['halftime_score', 'fulltime_score']] = df['detailed_score'].str.extract(r'\((.*?); (.*?)\)')
df[['home_score', 'away_score']] = df['fulltime_score'].str.split(':', expand=True).astype(int)

# Calculate the match results
df['gol_abs'] = df['home_score'] - df['away_score']
df['result'] = df['gol_abs'].apply(lambda x: '1' if x > 0 else 'X' if x == 0 else '2')

# Calculate the probabilities based on average odds
# Assuming that the average odds columns are named 'avg_odds_home_win', 'avg_odds_draw', and 'avg_odds_away_win'
# If these columns are not present, this part of the code will need to be adjusted accordingly
df['prob1'] = 1 / df['avg_odds_home_win']
df['probX'] = 1 / df['avg_odds_draw']
df['prob2'] = 1 / df['avg_odds_away_win']

# Define bins for segmenting the probabilities
bins = pd.cut(df['prob1'], bins=10, labels=False)
bin_centers = pd.cut(df['prob1'], bins=10).apply(lambda x: x.mid).unique()

# Calculate observed and mean predicted probabilities for each bin
observed = df.groupby(bins)['result'].apply(lambda x: (x == '1').mean())
predicted = df.groupby(bins)['prob1'].mean()

# Plot the scatter plot
plt.scatter(predicted, observed, label='home victory', color='blue')
plt.scatter(predicted, observed, label='draw', color='red')
plt.scatter(predicted, observed, label='away victory', color='green')
plt.xlabel('estimated prob')
plt.ylabel('observed prob')
plt.legend()
plt.title('Observed vs Predicted Probabilities')
plt.savefig('/workspace/result.png')
