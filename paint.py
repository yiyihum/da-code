import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.gridspec as gridspec

results_folder = 'dabench\\benchmark\\results\\results_analysis'
mapping_file = os.path.join(results_folder, 'mapping.csv')
mapping_df = pd.read_csv(mapping_file)
type_mapping = dict(zip(mapping_df['step_type'], mapping_df['class']))

# 保证colors与类别数目一致，可以修改颜色
category_colors = {
    "File Viewing": "#1e4c9c",
    "File Operating": "#345d82",
    "Data Processing": "#3371b3",
    "System Operations": "#5795c7",
    "Image & Display Operations": "#92b5ca",
    # "Archive & Compression Operations": "#81b5d5",
    "Package Management Operations": "#aed4e5",
    # "Network & Communication Operations": "#cce4ef",
    "New SQL Query": "#b83945",
    "New SQL": "#c25759",
    "New SQL Create": "#e69191",
    "Debug SQL Query": "#edb8b0",
    "Debug SQL": "#f5dfdb",
    "Debug SQL Create": "#fbdfe2",
    "New Python": "#4f845c",
    "Debug Python": "#cfe7c4",
    "Other": "#b696b6",
    "Action Parse Failed": "#f6c8a8"
}

excluded_types = {"Python", "Unknown"}
# 用于收集Unknown类型的数据
unknown_content = defaultdict(list)

# 用于存放所有图像的axes列表
axes_list = []

# 创建绘图网格
fig = plt.figure(figsize=(20, 15))  # 增大总图的高度
grid = gridspec.GridSpec(nrows=3, ncols=3, figure=fig, hspace=0.5)  # 调整子图的垂直间距

file_count = 0  # 用于计算处理的文件数量

for file_name in os.listdir(results_folder):
    if file_name.endswith('.csv') and file_name != 'mapping.csv':
        file_path = os.path.join(results_folder, file_name)
        
        # 读取CSV文件
        df = pd.read_csv(file_path)
        
        # 初始化数据结构
        turns = list(range(1, df.shape[1]))  # 步数，跳过第一列
        type_counts = defaultdict(lambda: [0] * len(turns))

        # 统计每一步出现的类型数量
        for turn_index, column in enumerate(df.columns[1:]):  # 跳过第一列
            for step in df[column].dropna():
                clazz = type_mapping.get(step, 'Unknown')
                if clazz not in excluded_types:
                    type_counts[clazz][turn_index] += 1
                elif clazz == 'Unknown':
                    unknown_content[file_name].append(step)

        if not type_counts:
            continue  # 如果type_counts为空，跳过

        # 转换数据用于绘图，按照category_colors的顺序
        type_counts = {k: v for k, v in type_counts.items() if k in category_colors}
        sorted_types = [k for k in category_colors if k in type_counts]
        count_df = pd.DataFrame({k: type_counts[k] for k in sorted_types}, index=turns)

        # 设置颜色，按照sorted_types的顺序
        colors = [category_colors[clazz] for clazz in sorted_types]

        # 绘制当前文件的堆叠条形图并保存
        ax = count_df.plot(kind='bar', stacked=True, figsize=(14, 8), color=colors, legend=False)
        ax.set_title(file_name.replace('.csv', ''))
        ax.set_xlabel('Turn')
        ax.set_ylabel('Count')
        ax.set_xticks(range(len(turns)))
        ax.set_xticklabels(turns, rotation=0)

        # 保存图像
        output_image = os.path.join(results_folder, file_name.replace('.csv', '.png'))
        plt.savefig(output_image)
        plt.close()

        # 添加当前的图像到总图的axes中
        ax = fig.add_subplot(grid[file_count])
        count_df.plot(kind='bar', stacked=True, ax=ax, color=colors, legend=False)
        ax.set_title(file_name.replace('.csv', ''))
        ax.set_xlabel('Turn')
        ax.set_ylabel('Count')
        ax.set_xticks(range(len(turns)))
        ax.set_xticklabels(turns, rotation=0)
        
        file_count += 1

# 调整布局并显示总图
fig.tight_layout(rect=[0, 0, 1, 0.8])  # 调整图例与子图的总布局

# 为总图添加图例，按照category_colors的顺序，并控制位置
handles = [plt.Line2D([0], [0], color=color, lw=4) for color in category_colors.values()]
labels = list(category_colors.keys())
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1), ncol=4)  # 调整图例的位置

overall_output_image = os.path.join(results_folder, 'all_results.png')
plt.savefig(overall_output_image, bbox_inches='tight')
plt.show()


# 输出Unknown的内容
for file, contents in unknown_content.items():
    print(f"Unknown contents in {file}:")
    for content in contents:
        print(f"  - {content}")