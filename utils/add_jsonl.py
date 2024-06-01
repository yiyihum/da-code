import pandas as pd


id = 'ml-competition-004'
source = 'https://www.kaggle.com/code/lucamassaron/steel-plate-eda-xgboost-is-all-you-need'
hints = """
1. analysis target data
2. use  feature engineering
3. choose xgboost classifiser
"""
instruction ="""
This is a dataset for a Steel plates data for defect prediction competition, with the description available in README.md. You are now a contestant in this competition and need to design a method to predict the data in test.csv according to the competition requirements. Write the results into submission.csv according to the format of sample_submission.csv."""

data_json =[{
    "id": id,
    "source":  source,
    "instruction": instruction,
    "hints": hints,
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
    "post_process": []
}]

# 保存为jsonl
import json
with open("./benchmark/configs/Competition.jsonl", "a") as f:
    for item in data_json:
        json.dump(item, f)
        f.write("\n")

