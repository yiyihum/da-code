import pandas as pd
import matplotlib.pyplot as plt

# Read the compressed CSV file containing the odds data
df = pd.read_csv('/workspace/closing_odds.csv.gz', compression='gzip', encoding='latin1')

# Calculate the match results
df['gol_abs'] = df['home_score'] - df['away_score']
df['result'] = df['gol_abs'].apply(lambda x: '1' if x > 0 else 'X' if x == 0 else '2')

# Calculate the probabilities based on average odds
df['prob1'] = 1 / df['avg_odds_home_win']
df['probX'] = 1 / df['avg_odds_draw']
df['prob2'] = 1 / df['avg_odds_away_win']

# Normalize the probabilities so they sum to 1
prob_sum = df[['prob1', 'probX', 'prob2']].sum(axis=1)
df['prob1'] /= prob_sum
df['probX'] /= prob_sum
df['prob2'] /= prob_sum

# Define bins for segmenting the probabilities
bins = pd.cut(df['prob1'], bins=10, labels=False)
bin_centers = pd.cut(df['prob1'], bins=10).apply(lambda x: x.mid).unique()

# Calculate observed and mean predicted probabilities for each bin
observed_home = df.groupby(bins)['result'].apply(lambda x: (x == '1').mean())
predicted_home = df.groupby(bins)['prob1'].mean()

observed_draw = df.groupby(bins)['result'].apply(lambda x: (x == 'X').mean())
predicted_draw = df.groupby(bins)['probX'].mean()

observed_away = df.groupby(bins)['result'].apply(lambda x: (x == '2').mean())
predicted_away = df.groupby(bins)['prob2'].mean()

# Plot the scatter plot
plt.scatter(predicted_home, observed_home, label='home victory', color='blue')
plt.scatter(predicted_draw, observed_draw, label='draw', color='red')
plt.scatter(predicted_away, observed_away, label='away victory', color='green')
plt.xlabel('estimated prob')
plt.ylabel('observed prob')
plt.legend()
plt.title('Observed vs Predicted Probabilities')
plt.savefig('/workspace/result.png')
