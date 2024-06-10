# Carrega os pacotes utilizados
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def missing_data(data):
    """
    Calculates information about missing data in a DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: A summary of missing data including total count, unique values,
                      null count, and percentage of missing values.
    """
    total = data.count()
    unique = data.nunique()
    null = data.isnull().sum()
    percent = round((data.isnull().sum() / data.isnull().count() * 100), 2)
    tt = pd.concat([total, unique, null, percent], axis=1, keys=['Total', 'Unique', 'Null', 'Percent'])
    types = []
    for col in data.columns:
        dtype = str(data[col].dtype)
        types.append(dtype)
    tt['Types'] = types
    return tt.transpose()

def count_by_column(df, count_column):
    """
    Counts occurrences of values and calculates the percentage in the specified count_column.

    Args:
        df (pandas.DataFrame): The input DataFrame.
        count_column (str): Column name for counting occurrences.

    Returns:
        pandas.DataFrame: A DataFrame with count of occurrences and percentage.
    """
    count = df[count_column].value_counts().reset_index()
    count.columns = [count_column, 'occurrences']  # Rename the columns for clarity
    count['percentage'] = round(100 * (count['occurrences'] / count['occurrences'].sum()), 2)
    return count

def freq_column(df, column):
    """
    Calculate the frequency distribution of a column in a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        column (str): The name of the column to analyze.

    Returns:
        pd.Series: A Series containing the frequency distribution.
    """
    n = len(df) #df size
    k = np.ceil(1 + 3.322 * np.log10(n)) #number of classes
    sorted_data = np.sort(df[column]) #sort value ascending
    data_range = np.max(sorted_data) - np.min(sorted_data) #range of df
    bin_width = np.ceil(data_range / k) #range of classes
    bins = [np.min(sorted_data) + i * bin_width for i in range(int(k) + 1)] #limits of classes
    freq = pd.cut(sorted_data, bins=bins, right=False).value_counts() #frequency's table
    freq_df = pd.DataFrame(freq)
    freq_df["Percentage"] = round((freq_df["count"] / n) * 100, 2)
    return freq_df

# Trazer os arquivos CSV para o Pandas
channels = pd.read_csv('Plot-pie-1\\channels.csv')
deliveries = pd.read_csv('Plot-pie-1\\deliveries.csv')
drivers = pd.read_csv('Plot-pie-1\\drivers.csv')
orders = pd.read_csv('Plot-pie-1\\orders.csv')
payments = pd.read_csv('Plot-pie-1\\payments.csv')

# Esses arquivos precisaram passar por um Encoding diferente para detectar os dados com acentuação.
hubs = pd.read_csv('Plot-pie-1\\hubs.csv', encoding="ISO-8859-2")
stores = pd.read_csv('Plot-pie-1\\stores.csv', encoding="ISO-8859-2")

# Junta algumas das tabelas de interesse para facilitar a visualização
# Processamento do dataframe 'deliveries'
df_entregas = deliveries.dropna(subset=['driver_id']).astype({'driver_id': 'int64'})
df_entregas = df_entregas.merge(drivers.set_index('driver_id'), on='driver_id')

# Processamento do dataframe 'stores'
df_lojas = stores.merge(hubs.set_index('hub_id'), on='hub_id', how='left')
df_lojas = df_lojas.drop(columns=[
    'store_latitude', 'store_longitude', 'hub_latitude',
    'hub_longitude', 'hub_id', 'hub_state'])

# Processamento do dataframe 'orders'
df_pedidos = orders.astype({'order_moment_created': 'datetime64[s]'})
df_pedidos = df_pedidos.drop(columns=[
    'order_created_minute', 'order_created_hour', 'order_created_day',
    'order_created_month', 'order_created_year', 'order_moment_accepted',
    'order_moment_ready', 'order_moment_collected', 'order_moment_in_expedition',
    'order_moment_delivering', 'order_moment_delivered', 'order_moment_finished',
    'order_metric_collected_time', 'order_metric_paused_time',
    'order_metric_production_time', 'order_metric_walking_time',
    'order_metric_expediton_speed_time', 'order_metric_transit_time',
    'order_metric_cycle_time'])
df_pedidos = df_pedidos.merge(channels.set_index('channel_id'), on='channel_id')
df_pedidos['data'] = df_pedidos['order_moment_created'].dt.strftime('%d-%m-%Y')
df_pedidos['mes_ano'] = df_pedidos['order_moment_created'].dt.strftime('%m-%Y')
df_pedidos['dia_semana'] = df_pedidos['order_moment_created'].dt.strftime('%A')
df_pedidos = df_pedidos.drop(columns=['order_moment_created'])

# Merge the processed dataframes to create the final dataframe for analysis
final_df = df_pedidos.merge(df_entregas.set_index('delivery_order_id'), on='delivery_order_id', how='left')
final_df = final_df.merge(df_lojas.set_index('store_id'), on='store_id', how='left')

# Filter the DataFrame for the city of CURITIBA
curitiba_df = final_df[final_df['hub_city'] == 'CURITIBA']

# Group by 'driver_modal' and count the number of orders for CURITIBA
curitiba_driver_df = curitiba_df.groupby('driver_modal')['order_id'].agg(order_count='count').reset_index()

# Calculate the total orders for CURITIBA
curitiba_driver_df['total'] = curitiba_driver_df['order_count'].sum()

# Calculate the percentage of orders for each driver modal in CURITIBA
curitiba_driver_df['percentage'] = (curitiba_driver_df['order_count'] / curitiba_driver_df['total'] * 100).round(2)

# Create a pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(curitiba_driver_df['percentage'], labels=curitiba_driver_df['driver_modal'], autopct='%1.1f%%', colors=sns.color_palette('autumn_r'))
ax.set_title('Percentage of orders delivered by type of driver in CURITIBA')

plt.savefig('result.jpg')
# Show the plot
plt.show()