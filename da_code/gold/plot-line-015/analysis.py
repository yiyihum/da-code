import pandas as pd
import matplotlib.pyplot as plt

# 读取 result.csv 文件
data = pd.read_csv('Plot-line-6\\gold\\result.csv')

# 设置日期为索引
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# 绘制图像
plt.figure(figsize=(12, 6))

plt.plot(data.index, data['Cumulative_EW'], label='Cumulative EW')
plt.plot(data.index, data['Cumulative_MCap'], label='Cumulative MCap')
plt.plot(data.index, data['Cumulative_MSR'], label='Cumulative MSR')
plt.plot(data.index, data['Cumulative_GMV'], label='Cumulative GMV')

plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.title('Cumulative Returns Over Time')
plt.legend()
plt.grid(True)
plt.savefig('result.jpg')
plt.show()