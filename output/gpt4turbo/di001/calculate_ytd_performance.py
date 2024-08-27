import pandas as pd
from datetime import datetime

# Define the tickers of the "Magnificent 7" stocks
magnificent_seven_tickers = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'FB', 'TSLA', 'NFLX']

# Load the stock price data and convert the DATE column to datetime
stock_prices = pd.read_csv('STOCK_PRICE_TIMESERIES.csv')
stock_prices['DATE'] = pd.to_datetime(stock_prices['DATE'])

# Filter for the "Magnificent 7" stocks and post-market close prices
filtered_prices = stock_prices[(stock_prices['TICKER'].isin(magnificent_seven_tickers)) &
                               (stock_prices['VARIABLE'] == 'post-market_close')]

# Get the current year
current_year = datetime.now().year

# Filter for the current year's data
ytd_prices = filtered_prices[filtered_prices['DATE'].dt.year == current_year]

# Get the earliest and latest dates in the current year
start_date = ytd_prices['DATE'].min()
end_date = ytd_prices['DATE'].max()

# Calculate the YTD performance for each stock
ytd_performance = []
for ticker in magnificent_seven_tickers:
    stock_data = ytd_prices[ytd_prices['TICKER'] == ticker]
    if not stock_data.empty:
        # Ensure there is data for both start and end dates
        if start_date in stock_data['DATE'].values and end_date in stock_data['DATE'].values:
            start_price = stock_data[stock_data['DATE'] == start_date]['VALUE'].iloc[0]
            end_price = stock_data[stock_data['DATE'] == end_date]['VALUE'].iloc[0]
            performance = ((end_price - start_price) / start_price) * 100
        else:
            performance = "Data not available for full YTD period"
    else:
        performance = "No data available"
    ytd_performance.append({'TICKER': ticker, 'YTD_Performance': performance})

# Convert the results to a DataFrame and save to CSV
ytd_performance_df = pd.DataFrame(ytd_performance)
ytd_performance_df.to_csv('/workspace/ytd_performance.csv', index=False)

# Output the path to the CSV file
print('/workspace/ytd_performance.csv')
