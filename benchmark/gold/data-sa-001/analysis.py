import pandas as pd
import pingouin as pg
from scipy.stats import shapiro
import json
import warnings
warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
women = pd.read_csv('../women_results.csv', index_col=0)
men = pd.read_csv('../men_results.csv', index_col=0)

# categorical columns
cat_col_women = [col for col in men.columns if men[col].dtypes == 'O']
cat_col_men = [col for col in men.columns if men[col].dtypes == 'O']

# removing "date" variable from categorical columns
cat_col_women = [col for col in cat_col_women if col not in 'date']
cat_col_men = [col for col in cat_col_men if col not in 'date']

# Converting datetype of the variable "date" to datetime
women['date'] = pd.to_datetime(women['date'])
men['date'] = pd.to_datetime(men['date'])

df_women = women.loc[(women['tournament'] == 'FIFA World Cup') & (women['date'] >= '2000-01-01')]
df_men = men.loc[(men['tournament'] == 'FIFA World Cup') & (men['date'] >= '2000-01-01')]

df_women['goals_scored'] = df_women['home_score'] + df_women['away_score']
df_men['goals_scored'] = df_men['home_score'] + df_men['away_score']

# Calculation of mean goal scores for women and determination of normality
statistic, p_value = shapiro(df_women['goals_scored'])

# Calculation of mean goal scores for men and determination of normality
statistic, p_value = shapiro(df_men['goals_scored'])

# using pingouin
result = pg.mwu(df_women['goals_scored'], df_men['goals_scored'], alternative="greater")
p_val = result['p-val'].values[0]

if p_val <= 0.01:
    result = 'reject'
else:
    result = 'fail to reject'

result_dict = {"p_val": p_val, "result": result}
with open('result.json', 'w') as fp:
    json.dump(result_dict, fp)