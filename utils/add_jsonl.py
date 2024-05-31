import pandas as pd


id = 'ml-cluster-001'
source = 'https://www.kaggle.com/datasets/sonalisingh1411/mallcustomersdataset'
hints = """
"1.Select the third and fourth columns of data to form a feature vector.
2. Standardize the variables using StandardScaler.
3. Choose the AgglomerativeClustering model.
4. gold result: silhouette: 0.553"
"""
instruction ="""
This is a dataset of annual income and spending scores in a mall. You need to perform clustering analysis on the annual income and spending scores based on this dataset. Write the clustering results into cluster.csv, where result.csv consists of 'Feature_i' (the ith value of the processed feature vector) and 'Cluster' column (the clustering label results).
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
with open("./benchmark/configs/Cluster.jsonl", "w") as f:
    for item in data_json:
        json.dump(item, f)
        f.write("\n")

