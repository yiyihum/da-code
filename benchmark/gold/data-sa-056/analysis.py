import pandas as pd

# 加载CSV文件
data = pd.read_csv('DC2-5\\gold\\frog_tongue.csv')

# 按照ID列对数据进行分组，并计算每一组的平均冲击力
average_impact_force_by_id = data.groupby('ID')['impact force (mN)'].mean()

# 输出每个ID的平均冲击力
print("每个ID的平均冲击力：")
print(average_impact_force_by_id)

# Make an array of translated impact forces: translated_force_b
translated_force_b = force_b - np.mean(force_b) + 0.55

# Take bootstrap replicates of Frog B's translated impact forces: bs_replicates
bs_replicates = draw_bs_reps(translated_force_b, np.mean, 10000)

# Compute fraction of replicates that are less than the observed Frog B force: p
p = np.sum(bs_replicates <= np.mean(force_b)) / 10000

# Print the p-value
print('p = ', p)
