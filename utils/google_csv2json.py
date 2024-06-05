import pandas as pd

def load_csv(file_path):
    return pd.read_csv(file_path)

# 使用方法：
file_path = "./benchmark/configs/Visual.csv"
data = load_csv(file_path)

# 保存为json
# {
#     "id": "kaggle067",
#     "source": "https://www.kaggle.com/datasets/nitishsharma01/olympics-124-years-datasettill-2020/code",
#     "instruction": "I have a dataset about earthquake-affected building damages. The dataset information can be found in the README.md file. Please help me predict the damage status of the buildings listed in the incomplete.csv file. Save the results to a file named prediction.csv with the following column names: building_id, damage_grade.",
#     "hardness": "level1",
#     "config": [
#         {
#             "type": "copy_all_subfiles",
#             "parameters": {
#                 "dirs": ["./benchmark/source/kaggle067/"
#                 ]
#             }
#         }
#     ],
#     "post_process": []
# }

data_json = []
for index, row in data.iterrows():
    id = str(row["id."])
    if id == "nan":
        break
    if not row["Refined Instruction"] or not row["Context details"]:
        continue
    data_json.append({
        "id": id,
        "source": row["Source"],
        "instruction": row["Refined Instruction"],
        "hints": row["Hints"],
        "hardness": "level1",
        "config": [
            {
                "type": "copy_all_subfiles",
                "parameters": {
                    "dirs": ["./benchmark/source/" + id
                             ]
                }
            }
        ],
        "post_process": ["plot_process"]
    })

# 保存为jsonl
import json
with open("./benchmark/configs/Visual.jsonl", "w") as f:
    for line in data_json:
        f.write(json.dumps(line) + "\n")
