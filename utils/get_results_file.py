import os
import json
import glob

experiment_name = "azure-visual0605"
output_path = f"./benchmark/_result/{experiment_name}/"
result_path = f"./benchmark/output/{experiment_name}/"
os.makedirs(output_path, exist_ok=True)

result_json_path = result_path + "*/dabench/result.json"

# 使用glob找到所有的result.json文件
result_json_files = glob.glob(result_json_path)

for result_json_file in result_json_files:
    # 复制result.json文件到resuresult_json_filelt_path
    new_result_json_file = result_json_file.replace(result_path, output_path)
    os.makedirs(os.path.dirname(new_result_json_file), exist_ok=True)
    os.system(f"cp {result_json_file} {new_result_json_file}")

    with open(result_json_file, "r") as f:
        result_files_dict = json.load(f)["result_files"]
        result_files = result_files_dict["added_files"]+result_files_dict["changed_files"]+result_files_dict["post_process_files"]
        for result_file in result_files:
            new_result_file = result_file.replace(result_path, output_path)
            os.makedirs(os.path.dirname(new_result_file), exist_ok=True)
            os.system(f"cp {result_file} {new_result_file}")

        

