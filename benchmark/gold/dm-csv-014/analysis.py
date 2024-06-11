import numpy as np
import pandas as pd 
import jsonlines
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

data = []
with jsonlines.open('../Musical_Instruments_5.jsonl') as reader:
    for obj in reader:
        data.append(obj)

df = pd.DataFrame(data)

def convert_to_list(str_lst):
    # 检查str_lst是否为字符串类型
    if isinstance(str_lst, str):
        # 如果是字符串，执行原有的转换逻辑
        return eval(str_lst)
    # 如果str_lst已经是列表或其他类型，直接返回
    return str_lst

        
def total_rating(lst_rating):
    return lst_rating[1] # y

def helpful_rating(lst_rating):
    return lst_rating[0] # x

df["helpful"] = df["helpful"].map(convert_to_list) # "[x,y]" -> [x,y]
df["total_ratings"] = df["helpful"].map(total_rating) # y
df["helpful"] = df["helpful"].map(helpful_rating) # x

df["helpful_no"] = df["total_ratings"] - df["helpful"]
up = df["helpful"].tolist()
down = df["helpful_no"].tolist()
comments = pd.DataFrame({"up": up, "down": down})

def wilson_lower_bound(up, down, confidence=0.95):
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

comments["wlb"] = comments.apply(lambda x: wilson_lower_bound(x["up"], x["down"]), axis=1)
df["wilson_lower_bound"] = comments["wlb"]
df_top_comments = df.sort_values("wilson_lower_bound",ascending=False)
# Select the top 3 summaries
top_3_summaries = df_top_comments["summary"].head(3)

# Open a file named 'result.txt' in write mode
with open('./result.txt', 'w') as file:
    # Iterate over each summary in the top 3 summaries
    for summary in top_3_summaries:
        # Write each summary to the file followed by a newline character
        file.write(summary + '\n')

