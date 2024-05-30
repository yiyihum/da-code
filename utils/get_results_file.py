import os
import json
import glob

output_path = "./benchmark/output/azure-ML-test/" 
result_path = "./benchmark/results/azure-ML-test/" 
os.makedirs(output_path, exist_ok=True)

result_json_path = output_path + "*/dabench/result.json"

# 使用glob找到所有的result.json文件
result_json_files = glob.glob(result_json_path)

for result_json_file in result_json_files:
    # 复制result.json文件到resuresult_json_filelt_path
    new_result_json_file = result_json_file.replace("output", "results")
    os.makedirs(os.path.dirname(new_result_json_file), exist_ok=True)
    os.system(f"cp {result_json_file} {new_result_json_file}")

    with open(result_json_file, "r") as f:
        result_files_dict = json.load(f)["result_files"]
        result_files = result_files_dict["added_files"]+result_files_dict["changed_files"]+result_files_dict["post_process_files"]
        for result_file in result_files:
            new_result_file = result_file.replace("output", "results")
            os.makedirs(os.path.dirname(new_result_file), exist_ok=True)
            os.system(f"cp {result_file} {new_result_file}")

        

