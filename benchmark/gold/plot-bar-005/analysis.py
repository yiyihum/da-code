import warnings
# warnings.filterwarnings('ignore')
import os
import re
import math
import glob
import itertools
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.figure_factory as ff

# Read the csvs
# survey_schema = pd.read_csv(input_dir/ 'SurveySchema.csv')
# freeFormResp = pd.read_csv(input_dir/ 'freeFormResponses.csv')
multiChoiceResp = pd.read_csv('../multipleChoiceResponses.csv')

color = sns.color_palette()

# For REPRODUCIBILITY
seed = 111
np.random.seed(seed)

def pct_on_bars(axs, df, offset=50, orientation='v', adjustment=2, pos='center', prec=1, fontsize=10):
    """
    This function can be used to plot percentage on each bar in a barplot. The function assumes
    that for each value on an axis, there is only one corresponding bar. So, if you have plotted something with
    hue, then you should consider using something else
    
    Arguments:
    axs: Matplotlib axis
    df: pandas dataframe used for this plot
    offset: Relative position of the text w.r.t the bar
    orientation: 'h' or 'v'
    adjustment: If the text overflows the bar on either side, you can adjust it by passing some value
    prec: How much precision is to be used for displaying percentage?
    fontsize: size of the font used in percentage text
    
    """
    
    # Get all the bars
    bars = axs.patches
    
    # Size of dataframe
    items = len(df)
    
    assert round(prec)>-1, "Precision value passed is wrong "
    
    # Iterate over each bar and plot the percentage
    for bar in bars:
        width = bar.get_width()
        height = bar.get_height()
        precision = '{0:.' + str(prec) + '%}'
        
        if math.isnan(width):
            width=0
        if math.isnan(height):
            height=0
        
        # Check orientation of the bars
        if orientation=='h':
            val_to_sub = height/adjustment
            axs.text(width + offset, bar.get_y()+bar.get_height()-val_to_sub, 
                    precision.format(width/items), ha=pos, fontsize=fontsize)
        
        elif orientation=='v':
            val_to_sub = width/adjustment
            axs.text(bar.get_x()+width-val_to_sub, height + offset, 
            precision.format(height/items), ha=pos, fontsize=fontsize)
        
        else:
            print("The orientation value you passed is wrong. It can either be horizontal 'h' or vertical 'v'")

# Select the column for the corresponding question
age_df = multiChoiceResp['Q2'][1:].dropna()
multiChoiceResp_cleanup = multiChoiceResp.dropna(subset=['Q2']).iloc[1:]

order= ['18-21', '22-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-69', '70-79', '80+']

f,ax=plt.subplots(figsize=(10,5))

# Do countplot 
ax = sns.countplot(x='Q2', data=multiChoiceResp_cleanup, order=order)

# plot the percentage on bars
pct_on_bars(ax, age_df, orientation='v', offset=50, adjustment=2)

# 删除数据标签
for text in ax.texts:
    text.set_visible(False)

plt.xlabel('Age Group')
plt.ylabel('Count')
plt.title('Age Group Distribution')
plt.savefig('result.png')
plt.show()
