import os
import pandas as pd
from collections import Counter

# 定义目录路径
input_dir = 'dabench\\benchmark\\results\\results_analysis'

# 初始化步骤计数器
step_counter = Counter()
# 遍历文件夹下所有的CSV文件
for filename in os.listdir(input_dir):
    if filename.endswith('.csv'):
        filepath = os.path.join(input_dir, filename)
        print(f"Found CSV file: {filepath}")

        # 如果你想在这里对CSV文件进行处理，可以使用pd.read_csv()
        df = pd.read_csv(filepath)
        # 遍历每个步骤进行计数
        for col in df.columns[1:]:  # 跳过第一列 (id)
            steps = df[col].dropna().tolist()
            step_counter.update(steps)       
# 将计数结果转换为DataFrame
step_df = pd.DataFrame.from_dict(step_counter, orient='index', columns=['count'])

# 写入步骤统计结果到CSV文件
step_df.to_csv('step_counts.csv', index_label='step')

import pandas as pd
from collections import defaultdict
# 读入数据
df = pd.read_csv('step_counts.csv')

# 确认 'step' 列是否有缺失数据，填充空白字符
df['step'] = df['step'].fillna('')

# 提取主要任务类型和子类型
df['main_type'] = df['step'].apply(lambda x: '-'.join(x.split('-')[:2]) if '-' in x else x)
df['sub_type'] = df['step'].apply(lambda x: x.split('-')[2] if x.count('-') > 1 else '')

# 初始化字典存储统计信息
stats = defaultdict(lambda: defaultdict(int))

# 统计每个主要任务类型及子类型的数量
for _, row in df.iterrows():
    main_type = row['main_type']
    sub_type = row['sub_type']
    stats[main_type][sub_type] += int(row['count'])

# 创建结果 DataFrame
results = []

for main_type, sub_types in stats.items():
    for sub_type, count in sub_types.items():
        results.append([main_type, sub_type, count])

result_df = pd.DataFrame(results, columns=['main_type', 'sub_type', 'count'])

result_df.to_csv('task_counts.csv', index=False)