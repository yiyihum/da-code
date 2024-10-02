import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv(f'../score.csv')
data.head()

def combinedplot(data, label, binwidth, figsize = (6, 6)):
    """
    Plot a combined `boxplot`, `histplot` and `rugplot` over the `data[label]`.

    Parameters
    ----------
    data : pd.DataFrame()
           data source to plot
    label : str
            designated label in `data` to plot
    binwidth : float, optional
               `binwidth` in `sns.histplot`
    figsize : tuple, default:(6, 6)
    """
    # initialize figure and axes
    fig, (ax_box, ax_hist) = plt.subplots(2, 1, figsize=figsize, sharex='col', 
                                          gridspec_kw={"height_ratios": (.15, .85)})
    
    # boxplot
    sns.boxplot(data=data, x=label, ax=ax_box, color='crimson')

    # histplot
    sns.histplot(data=data, x=label, ax=ax_hist, binwidth=binwidth)

    # rugplot
    sns.rugplot(data=data, x=label, ax=ax_hist, height=0.05, 
                color='gold', 
                lw=2.)
    
    plt.tight_layout()
    
    return None

old_label = ['Hours', 'Scores']
new_label = ['Time (hr)', 'Score']

data.rename(columns=dict(zip(old_label, new_label)), inplace=True)
data.head()

print(f'Value counts: {data.isnull().value_counts()}\n\nData shape: {data.shape}')

data.describe()
combinedplot(data, 'Time (hr)', binwidth=0.5)
combinedplot(data, 'Score', binwidth=5.)
data.corr()

plt.show()