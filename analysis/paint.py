import os
import pandas as pd
import matplotlib.pyplot as plt

# 定义的颜色字典
category_colors = {
    "File Viewing": "#000080",  
    "File Operating": "#6640ff",  
    "Data Processing": "#1e90ff",  
    "System Operations": "#66ffe6", 
    "Package Management": "#a6ffcc",  
    "SQL Query": "#008b8b",  
    "SQL Update": "#d2b48c",   
    "SQL Debug": "#9acd32",  
    "Python": "#ff4d40",  
    "Python Debug": "#ff8c69",  
    "Other": "#e68ab8"  
}

# 有序的类别列表
ordered_categories = [
    "File Viewing",  
    "File Operating",  
    "Data Processing",  
    "System Operations", 
    "Package Management Operations",  
    "SQL Query",  
    "SQL",  
    "SQL Create",  
    "SQL Debug",  
    "Python",  
    "Python Debug",  
    "Other"  
]

# 指定数据目录
results_folder = 'analysis\counts_for_turn'
output_folder = 'analysis\images'
# 遍历目录中的所有统计文件
for file_name in os.listdir(results_folder):
    if file_name.endswith('_counts.csv'):
        file_path = os.path.join(results_folder, file_name)
        
        # 将CSV文件读取到DataFrame
        df = pd.read_csv(file_path)
        
        # 将'Round'列设置为索引
        df.set_index('Round', inplace=True)
        
        # 确保列的存在，过滤不存在的类别
        available_categories = [col for col in ordered_categories if col in df.columns]
        
        # 为存在的列生成颜色列表
        color_list = [category_colors[col] for col in available_categories]
        
        # 创建堆叠图
        ax = df[available_categories].plot(kind='bar', stacked=True, figsize=(7, 6), color=color_list)
        
        # 设置图例位置
        ax.legend(loc='upper right')
        
        # 设置标题
        plt.title(file_name.replace('_counts.csv', ''))
        
        # 设置标签
        plt.xlabel('Round')
        plt.ylabel('Counts')
        
        # 调整布局
        plt.tight_layout()
        
        # 显示图表
        plt.savefig(os.path.join(output_folder, file_name.replace('_counts.csv', '.png')))
        plt.close()  # 关闭图表，避免占用过多资源

# import os
# import pandas as pd
# import matplotlib.pyplot as plt

# # 指定数据目录
# results_folder = 'dabench\\benchmark\\results\\results_analysis'

# # 遍历目录下的所有统计文件
# for file_name in os.listdir(results_folder):
#     if file_name.endswith('_counts.csv'):
#         file_path = os.path.join(results_folder, file_name)
        
#         # 读取 CSV 文件
#         df = pd.read_csv(file_path)
        
#         # 将 'Round' 列设置为索引
#         df.set_index('Round', inplace=True)
        
#         # 创建堆叠图
#         ax = df.plot(kind='bar', stacked=True, figsize=(10, 6))
        
#         # 设置图例
#         ax.legend(loc='upper left', bbox_to_anchor=(1,1))
        
#         # 设置标题，以文件名作为图的标题
#         plt.title(file_name.replace('_counts.csv', ''))
        
#         # 设置标签
#         plt.xlabel('Round')
#         plt.ylabel('Counts')
        
#         # 调整布局以便显示图例
#         plt.tight_layout()
        
#         # 显示图表
#         plt.show()