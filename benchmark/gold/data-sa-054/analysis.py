import numpy as np
def bootstrap_replicate_1d(data, func):
    """Generate bootstrap replicate of 1D data."""
    bs_sample = np.random.choice(data, len(data))
    return func(bs_sample)

def draw_bs_reps(data, func, size=1):
    """Draw bootstrap replicates."""

    # Initialize array of replicates: bs_replicates
    bs_replicates = np.empty(size)

    # Generate replicates
    for i in range(size):
        bs_replicates[i] = bootstrap_replicate_1d(data, func)

    return bs_replicates

import pandas as pd

# 假设txt文件名为weather_data.txt，并且数据以空格分隔
filename = 'DC2-3\\gold\\sheffield_weather_station_cleaned.csv'

# 读取数据，假定列已按照空格分隔，并且没有列名
df = pd.read_csv(filename, delim_whitespace=True, header=None)

# 提供列名以便于理解数据
df.columns = ['year', 'month', 'tmax', 'tmin', 'af', 'rain', 'sun']

# 去掉不包含数值数据的第一行
df = df.iloc[1:]

# 转换列 'year' 为整形，'rain' 为浮点型
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['rain'] = pd.to_numeric(df['rain'], errors='coerce')

# 删除因无法转换而产生的NaN值所在行
df.dropna(subset=['year', 'rain'], inplace=True)

# 计算每年降水量的总和
annual_rainfall_sum = df.groupby('year')['rain'].sum()

# 结果是一个Series, 如果你需要的是DataFrame类型, 可以进行转换
annual_rainfall_sum_df = annual_rainfall_sum.reset_index()

# 将'rain'列设置为浮点数
annual_rainfall_sum_df['rain'] = annual_rainfall_sum_df['rain'].astype(float)

# 打印结果
rainfall = annual_rainfall_sum_df["rain"].to_numpy()[:-1]

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Assuming draw_bs_reps function is defined
# Assuming rainfall data is defined and bs_replicates is generated as shown in your code

# Generate 10,000 bootstrap replicates of the variance: bs_replicates
bs_replicates = draw_bs_reps(rainfall, np.var, size=10000)

# Put the variance in units of square centimeters
bs_replicates /= 100

# Calculate the histogram: counts and bin edges
counts, bin_edges = np.histogram(bs_replicates, bins=50, density=True)

# Calculate bin centers
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Calculate the probability density values
pdf_values = counts

# Create a DataFrame to store bin centers and PDF values
pdf_data = pd.DataFrame({
    'Bin Center': bin_centers,
    'PDF': pdf_values
})

# Save the DataFrame to a CSV file
pdf_data.to_csv('bootstrap_variance_pdf.csv', index=False)

# Plotting for visualization (optional)
_ = plt.hist(bs_replicates, bins=50, density=True)
_ = plt.xlabel('variance of annual rainfall (sq. cm)')
_ = plt.ylabel('PDF')
plt.show()
