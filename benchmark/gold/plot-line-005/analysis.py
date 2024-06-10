import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

import plotly
import plotly.express as px
import plotly.graph_objs as gobj
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
from collections import Counter

import statsmodels.api as sm
import scipy.stats.distributions as dist
from scipy.stats import t,ttest_rel
from statsmodels.stats.weightstats import ztest

from warnings import simplefilter
simplefilter("ignore")

data15 = pd.read_csv('../2015.csv');  
data16 = pd.read_csv('../2016.csv');  
data17 = pd.read_csv('../2017.csv');  
data18 = pd.read_csv('../2018.csv');  
data19 = pd.read_csv('../2019.csv');  

collection = [data15,data16,data17,data18,data19]

# Naming the datasets
data15.name = 'data15'
data16.name = 'data16'
data17.name = 'data17'
data18.name = 'data18'
data19.name = 'data19'

data_scores = pd.DataFrame()
DS = pd.DataFrame()

data_scores[['country','region','2015_rank','2015_score']] = data15[['Country','Region','Happiness Rank','Happiness Score']]

d16 = pd.DataFrame()
d17 = pd.DataFrame()
d18 = pd.DataFrame()
d19 = pd.DataFrame()

d16[['country','2016_rank','2016_score']] = data16[['Country','Happiness Rank','Happiness Score']]
d17[['country','2017_rank','2017_score']] = data17[['Country','Happiness.Rank','Happiness.Score']]
d18[['country','2018_rank','2018_score']] = data18[['Country or region','Overall rank','Score']]
d19[['country','2019_rank','2019_score']] = data19[['Country or region','Overall rank','Score']]
data_scores = data_scores.merge(d16,on=['country'])
data_scores = data_scores.merge(d17,on=['country'])
data_scores = data_scores.merge(d18,on=['country'])
data_scores = data_scores.merge(d19,on=['country'])

x = [2015,2016,2017,2018,2019]
y1 = [7.285000,7.323500,7.299000,7.298000,7.267500]
y2 = [7.273000,7.254000,7.154500,7.107000,7.085000]
y3 = [6.739350,6.731400,6.748400,6.829100,6.898400]
y4 = [6.137300,6.050500,5.947400,5.937750,5.942550]
y5 = [5.496250,5.477000,5.496500,5.540250,5.564250]
y6 = [5.372625,5.396750,5.444875,5.399750,5.333375]
y7 = [5.344571,5.379607,5.418321,5.473929,5.571786]
y8 = [5.330789,5.386053,5.369684,5.282737,5.237000]
y9 = [4.580857,4.563286,4.628429,4.603857,4.526857]
y10 = [4.120419,4.074839,4.131129,4.247968,4.380323]

plt.figure(figsize=(12,6))
plt.plot(x, y1, '-o', label='ANZ')  # Australia and New Zealand
plt.plot(x, y2, '-o', label='NA')   # North America
plt.plot(x, y3, '-o', label='WEU')  # Western Europe
plt.plot(x, y4, '-o', label='LAC')  # Latin America and Caribbean
plt.plot(x, y5, '-o', label='EA')   # Eastern Asia
plt.plot(x, y6, '-o', label='SEA')  # Southeastern Asia
plt.plot(x, y7, '-o', label='CEE')  # Central and Eastern Europe
plt.plot(x, y8, '-o', label='MENA') # Middle East and Northern Africa
plt.plot(x, y9, '-o', label='SA')   # Southern Asia
plt.plot(x, y10, '-o', label='SSA') # Sub-Saharan Africa


plt.title('Happiness Scores in 2015-2019')
plt.xticks(fontsize=14)
plt.legend(loc='upper left',fontsize=8);

plt.savefig('result.png')

