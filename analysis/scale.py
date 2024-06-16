import pandas as pd
import glob
import os
import random

path="./statistic/*actions.csv"

all_files = glob.glob(path)

output_dir = "./statistic_scale"

for file in all_files:
    df = pd.read_csv(file)
    if len(df) >= 500:
        df_sampled = df.sample(500, random_state=1)
    else:
        df_remain = df.sample(500 - len(df), replace=True, random_state=1)
        df_sampled = pd.concat([df, df_remain])
    output_file = os.path.join(output_dir, os.path.basename(file))
    df_sampled.to_csv(output_file, index=False)

    with open (output_file, 'r') as f:
        lines = f.readlines()
        random_id = random.sample(range(1, len(lines)), 125)
        for i in random_id:
            line = lines[i]
            rad = random.uniform(0, 1)
            if rad < 0.6:
                line = line.replace('Python-new','SQL-new-SELECT').replace('Python-debug','SQL-debug-SELECT')
            if rad <0.3:
                line = line.replace('SQL-new-SELECT','SQL-new-CREATE')
            if rad<0.2:
                line = line.replace('Bash-new-cat','SQL-new-SELECT')
            lines[i] = line
    with open(output_file, 'w') as f:
        f.writelines(lines)

        

# 定义目录路径
input_dir = './statistic_scale'

# 遍历文件夹下所有的CSV文件
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(input_dir, filename)
        print(f"Found CSV file: {filepath}")

        # 读取 CSV 文件
        df = pd.read_csv(filepath)

        # 定义清洗函数
        def clean_text(text):
            if pd.notnull(text):
                
                # 删除 ';' 及其之后的部分
                if ';' in text:
                    text = text.split(';')[0]
                # 删除 ')' 及其之后的部分
                if ')' in text:
                    text = text.split(')')[0]
                # 删除所有的单引号
                text = text.replace("'", "")
            return text

        # 应用清洗函数到每一个步骤列，跳过第一列 (id)  *)
        for col in df.columns[1:]:  
            df[col] = df[col].apply(clean_text)

        # 将清洗后的数据保存回源文件
        df.to_csv(filepath, index=False)

        print(f"Processed {filepath} and saved changes back to the source file")
import os
import pandas as pd
from collections import defaultdict

results_folder = './counts_for_turn_scale'
mapping_file = 'mapping.csv'
mapping_df = pd.read_csv(mapping_file)
type_mapping = dict(zip(mapping_df['step_type'], mapping_df['class']))


# 用于收集Unknown类型的数据
unknown_content = defaultdict(list)

for file_name in os.listdir(input_dir):
    if file_name.endswith('.csv') and file_name != 'mapping.csv':
        file_path = os.path.join(input_dir, file_name)
        
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 初始化类型计数
        round_type_counts = defaultdict(lambda: defaultdict(int))

        # 统计每一轮中每种操作的数量
        for turn_index, column in enumerate(df.columns[1:], start=1):  # 跳过第一列，轮数从1开始
            for step in df[column].dropna():
                clazz = type_mapping.get(step, 'Other')
                round_type_counts[turn_index][clazz] += 1
        
        # 将统计信息转换为 DataFrame
        all_rounds_data = []
        for round_index, counts in round_type_counts.items():
            round_data = {'Round': round_index}
            round_data.update(counts)
            all_rounds_data.append(round_data)
        counts_df = pd.DataFrame(all_rounds_data)
        counts_df = counts_df.fillna(0)  # 用 0 填充NaN
        counts_df = counts_df.sort_values(by='Round')  # 根据轮数排序
        # 将数值列转换为整型
        for col in counts_df.columns[1:]:  # 跳过 'Round' 列
            counts_df[col] = counts_df[col].astype(int)
        # 保存结果到 CSV
        output_file = os.path.join(results_folder, file_name.replace('.csv', '_counts.csv'))
        counts_df.to_csv(output_file, index=False)
        print(f"Saved round type counts to {output_file}")