import pandas as pd

def load_csv(file_path):
    return pd.read_csv(file_path)

# 使用方法：
file_path = "./benchmark/configs/DM.csv"

is_verbose = False

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
print(data.columns)
for index, row in data.iterrows():
    id = str(row["id."])
    if 'dm-csv' not in id:
        continue
    
    if not is_verbose:
        data_json.append({
            "id": id,
            "source": row["Source"],
            "instruction": row["Refined Instruction"],
            "hints": None,
            "hardness": row["Level"],
            "config": [
                {
                    "type": "copy_all_subfiles",
                    "parameters": {
                        "dirs": ["./benchmark/source/" + id
                                ]
                    }
                }
            ],
            "post_process": []
        })
    if is_verbose and row["Level"].lower() == "hard":
        verbose = row["Verbose"]
        ins_verbose = "\n\n[Verbose]\n" + verbose
        
        data_json.append({
            "id": id,
            "source": row["Source"],
            "instruction": row["Refined Instruction"] + ins_verbose,
            "hints": None,
            "hardness": "Hard",
            "config": [
                {
                    "type": "copy_all_subfiles",
                    "parameters": {
                        "dirs": ["./benchmark/source/" + id
                                ]
                    }
                }
            ],
            "post_process": []
        })
    
# 保存为jsonl
import json, jsonlines
data_json = sorted(data_json, key=lambda x: x["id"])
with jsonlines.open('./benchmark/configs/DM.jsonl', mode='w') as writer:
    for item in data_json:
        writer.write(item)
