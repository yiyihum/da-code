import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the compressed CSV file
file_path = 'closing_odds.csv.gz'
df = pd.read_csv(file_path, compression='gzip')

# Calculate the match results
df['gol_abs'] = df['home_score'] - df['away_score']
df['result'] = np.where(df['gol_abs'] > 0, '1', np.where(df['gol_abs'] < 0, '2', 'X'))

# Calculate the probabilities based on average odds
df['prob1'] = 1 / df['avg_odds_home_win']
df['probX'] = 1 / df['avg_odds_draw']
df['prob2'] = 1 / df['avg_odds_away_win']

# Normalize the probabilities
prob_sum = df[['prob1', 'probX', 'prob2']].sum(axis=1)
df['prob1'] /= prob_sum
df['probX'] /= prob_sum
df['prob2'] /= prob_sum

# Define bins for the probabilities
n_bins = 10
bins = np.linspace(0, 1, n_bins + 1)

# Compute observed and mean predicted probabilities for each bin
observed_probs = []
predicted_probs = []

for i in range(n_bins):
    bin_mask = (df['prob1'] >= bins[i]) & (df['prob1'] < bins[i+1])
    bin_df = df[bin_mask]
    observed = bin_df['result'].value_counts(normalize=True)
    predicted = bin_df[['prob1', 'probX', 'prob2']].mean()
    observed_probs.append(observed)
    predicted_probs.append(predicted)

# Prepare data for scatter plot
labels = ["home victory", "draw", "away victory"]
x_data = [p['prob1'] for p in predicted_probs]
y_data = [o.get('1', 0) for o in observed_probs]

# Create scatter plot
plt.scatter(x_data, y_data, label=labels[0])
plt.xlabel("estimated prob")
plt.ylabel("observed prob")
plt.title("Scatter Plot of Estimated vs Observed Probabilities")
plt.legend()
plt.grid(True)

# Save the plot
plt.savefig('result.png')
