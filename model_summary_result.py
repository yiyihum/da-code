import os
import json
import pandas as pd

def is_solid_action(action_type):
    """判断是否为 solid action。"""
    return action_type != "None"

def is_executable_code(action_type, action_result):
    """判断是否为 executable code。"""
    return action_type in ["Bash", "Python", "SQL"] and action_result != "error message"

def analyze_model_results(input_dir):
    # 初始化模型统计结果的字典
    model_results = []

    for filename in os.listdir(input_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(input_dir, filename)

            with open(filepath, 'r') as file:
                data = json.load(file)

            solid_actions = 0
            executable_codes = 0
            total_actions = 0

            # 遍历每个操作
            for example in data['results']:
                actions = example['actions']
                for action in actions:
                    action_type = action[0]
                    action_result = action[2]
                    total_actions += 1

                    if is_solid_action(action_type):
                        solid_actions += 1
                    if is_executable_code(action_type, action_result):
                        executable_codes += 1

            # 计算比例
            solid_action_ratio = solid_actions / total_actions if total_actions > 0 else 0
            executable_code_ratio = executable_codes / total_actions if total_actions > 0 else 0
            
            # 添加到结果字典
            model_results.append({
                "Model": filename.replace('_result.json', ''),
                "Solid_Action_Ratio": solid_action_ratio,
                "Executable_Code_Ratio": executable_code_ratio
            })

    # 创建 DataFrame 并保存到 CSV
    df = pd.DataFrame(model_results)
    df.to_csv(os.path.join(input_dir, 'model_summary_results.csv'), index=False)
    print("Model analysis completed and saved to 'model_summary_results.csv'.")

# 调用函数进行分析
input_dir = 'dabench\\benchmark\\results'
analyze_model_results(input_dir)