import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df1 = pd.read_csv('../closing_odds.csv.gz', index_col=0, compression='gzip')
def result1X2(x):
    if x>0:
        return '1'
    elif x == 0:
        return 'X'
    else:
        return '2'

df1['gol_abs'] = df1.home_score - df1.away_score
df1['result'] = df1.gol_abs.apply(result1X2)

def compute_probs(df_, odd1, oddX, odd2):
    p1 = 'prob1'
    pX = 'probX'
    p2 = 'prob2'
    df_[p1] = 1./df_[odd1]
    df_[pX] = 1./df_[oddX]
    df_[p2] = 1./df_[odd2]
    
    return df_


df1 = compute_probs(df1, 'avg_odds_home_win', 'avg_odds_draw', 'avg_odds_away_win')
def compute_accuracy_and_mean(df_, min_games, n_bins, p1, pX, p2):
    #compute the observed and consensus probabilities
    mean_obs1 = []
    mean_obsX = []
    mean_obs2 = []
    mean_cons1 = []
    mean_consX = []
    mean_cons2 = []
    bins = np.linspace(0,1,n_bins+1)
    
    #pdb.set_trace()
    
    
    for i,bn in enumerate(bins[:-1]):
        # Get the data from the bin
        boole1 = (df_[p1] > bn) & (df_[p1] <= bins[i + 1])
        booleX = (df_[pX] > bn) & (df_[pX] <= bins[i + 1])
        boole2 = (df_[p2] > bn) & (df_[p2] <= bins[i + 1])
        
        # Get accuracy for home, draw away
        if (boole1.sum() >= min_games):
            mean_obs1.append((df_.loc[boole1, 'result'] == '1').sum().astype(float) / boole1.sum())
            mean_cons1.append(df_.loc[boole1, p1].mean())
        else:
            mean_obs1.append(np.nan)
            mean_cons1.append(np.nan)

        if (booleX.sum() >= min_games):
            mean_obsX.append((df_.loc[booleX, 'result'] == 'X').sum().astype(float) / booleX.sum())
            mean_consX.append(df_.loc[booleX, pX].mean())
        else:
            mean_obsX.append(np.nan)
            mean_consX.append(np.nan)
            
        if (boole2.sum() >= min_games):
            mean_obs2.append((df_.loc[boole2, 'result'] == '2').sum().astype(float) / boole2.sum())
            mean_cons2.append(df_.loc[boole2, p2].mean())
        else:
            mean_obs2.append(np.nan)
            mean_cons2.append(np.nan)

        mean_obs_dict = {'1':mean_obs1, 'X':mean_obsX, '2':mean_obs2}
        mean_cons_dict = {'1':mean_cons1, 'X':mean_consX, '2':mean_cons2}
    
    return mean_obs_dict, mean_cons_dict
mean_obs_dict, mean_cons_dict = compute_accuracy_and_mean(df1, 100, 80,'prob1', 'probX', 'prob2')
plt.figure()
plt.scatter(mean_cons_dict['1'], mean_obs_dict['1'], c='blue', s=3, label='home victory')
plt.scatter(mean_cons_dict['X'], mean_obs_dict['X'], c='green', s=3, label='draw')
plt.scatter(mean_cons_dict['2'], mean_obs_dict['2'], c='red', s=3, label='away victory')
plt.xlabel('estimated prob')
plt.ylabel('observed prob')
plt.legend()
plt.savefig('./result.png')


