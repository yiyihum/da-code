import pandas as pd


id = 'ml-competition-009'
source = 'https://www.kaggle.com/code/rohangulati14/leading-sol-regression-with-an-abalone-dataset'
hints = """
"1. Remove the id column from the training and testing data.
2. Merge the original training data with the new training data.
3. Remove duplicate values.
4. Train a stacked regression model."
"""
instruction ="""
This is a competition based on an abalone dataset, with the description available in README.md. As a participant, you need to design a solution to complete this competition. Write your prediction results into submission.csv following the format of sample_submission.csv.
"""

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

