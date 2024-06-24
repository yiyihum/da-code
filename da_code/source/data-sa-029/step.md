To perform delta hedging for an investment portfolio with IBM stock using a European put option, follow these steps:

1. **Load and preprocess the stock price data**:
   - Load the historical stock price data from the CSV file.
   - Parse the 'date' column as dates and set it as the index.

2. **Calculate daily returns**:
   - Compute the daily percentage change in 'close' prices to get the returns.

3. **Compute annualized volatility**:
   - Calculate the annualized standard deviation of the daily returns to determine the volatility.

4. **Value the European put option using the Black-Scholes model**:
   - Set the spot price (S) to 70.
   - Set the strike price (X) to 80.
   - Set the time to maturity (T) to 0.5 years.
   - Set the risk-free interest rate (r) to 2%.
   - Use the calculated volatility (sigma).
   - Compute the option value for a put option.

5. **Calculate the delta of the option**:
   - Use the same parameters as in step 4 to calculate the delta of the put option.

6. **Determine the change in option value for a new stock price**:
   - Set the new stock price (S) to 69.5.
   - Use the same parameters as in step 4, but with the new stock price, to compute the new option value.
   - Calculate the change in option value by subtracting the original option value from the new option value.

7. **Calculate and print the delta hedge result**:
   - Compute the change in stock price (69.5 - 70).
   - Adjust the change in option value by dividing it by the delta.
   - Sum the change in stock price and the adjusted change in option value.
   - Print the result.
