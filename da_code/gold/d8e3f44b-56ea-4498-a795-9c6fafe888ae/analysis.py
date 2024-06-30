# Import library
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

df_population = pd.read_csv("../world_population.csv")
def cal_population_projection(df, start_year, target_year):
    start_year_pop = str(start_year) + " Population"
    target_year_pop = str(target_year) + " Population"
    start_year_gr = str(start_year) + " Growth Rate"
    df[target_year_pop] = df[start_year_pop] * ((1 + (df[start_year_gr]/100)) ** (target_year - start_year))
    df[target_year_pop] = df[target_year_pop].astype(int)
    return df

def cal_gr_estimation(df, start_year, target_year):
    start_year_pop = str(start_year) + " Population"
    target_year_pop = str(target_year) + " Population"
    target_year_gr = str(target_year) + " Growth Rate"
    df[target_year_gr] = ((df[target_year_pop]/df[start_year_pop]) ** (1/(target_year-start_year)) - 1) * 100
    return df

def cal_density(df, year):
    den_year = str(year) + " Density (per km²)"
    pop_year = str(year) + " Population"
    df[den_year] = df[pop_year] / df["Area (km²)"]
    return df

def cal_pop_percentage(df, year):
    pop_percentage_year = str(year) + " World Population Percentage"
    pop_year = str(year) + " Population"
    df[pop_percentage_year] = (df[pop_year] / df[pop_year].sum()) * 100
    return df

# Rename and Change Current Columns
df_population = df_population.rename(columns={"Growth Rate": "2022 Growth Rate"})
df_population["1970 Growth Rate"] = "Unknown"
df_population["2022 Growth Rate"] = (df_population["2022 Growth Rate"] - 1) * 100
df_population = df_population.rename(columns={"Density (per km²)": "2022 Density (per km²)"})
df_population = df_population.rename(columns={"World Population Percentage": "2022 World Population Percentage"})

# Calculate Population Projection
target_year = [2030, 2040, 2050]
for year in target_year:
    df_population = cal_population_projection(df_population, 2022, year)

# Calculate Growth Rate
start_year = [1970, 1980, 1990, 2000, 2010, 2015, 2022, 2022, 2022]
target_year = [1980, 1990, 2000, 2010, 2015, 2020, 2030, 2040, 2050]
for i in range(len(target_year)):
    df_population = cal_gr_estimation(df_population, start_year[i], target_year[i])

target_year = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2030, 2040, 2050]
# Calculate Density
for i in range(len(target_year)):
    df_population = cal_density(df_population, target_year[i])

# Calculate World Population Percentage
for i in range(len(target_year)):
    df_population = cal_pop_percentage(df_population, target_year[i])
print(df_population.head())