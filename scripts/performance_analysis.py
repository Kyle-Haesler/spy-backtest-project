from ema_strategy import df as backtest
import pandas as pd
import numpy as np

annual_trading_days = 252
annual_risk_free_rate = .05
daily_risk_free_rate = (1+ annual_risk_free_rate)**(1/annual_trading_days)
rolling_window = 21

# Calculate performance metrics
# Calculate cumulative returns
backtest["Strategy_Cum_Return"] = backtest["Account_Value"] / backtest["Account_Value"].iloc[0] - 1
backtest["Buy_Hold_Cum_Return"] = backtest["Buy_and_Hold_Account_Value"] / backtest["Buy_and_Hold_Account_Value"].iloc[0] - 1

# Calculate daily returns
backtest["Strategy_Daily_Return"] = backtest["Account_Value"].pct_change()
backtest["Buy_Hold_Daily_Return"] = backtest["Buy_and_Hold_Account_Value"].pct_change()

# Calculate Volatility
backtest["Strategy_Volatility"] = backtest["Strategy_Daily_Return"].rolling(window=rolling_window).std() * np.sqrt(annual_trading_days)
backtest["Buy_Hold_Volatility"] = backtest["Buy_Hold_Daily_Return"].rolling(window=rolling_window).std() * np.sqrt(annual_trading_days)

# Daily returns less the risk free rate
strategy_excess = backtest["Strategy_Daily_Return"] - daily_risk_free_rate
buy_hold_excess = backtest["Buy_Hold_Daily_Return"] - daily_risk_free_rate

# Calculate Annualized Sharpe Ratios
backtest["Strategy_Sharpe"] = (strategy_excess.mean() / strategy_excess.std()) * np.sqrt(annual_trading_days)
backtest["Buy_Hold_Sharpe"] = (buy_hold_excess.mean() / buy_hold_excess.std()) * np.sqrt(annual_trading_days)

# Calculate rolling Sharpe Ratios over period
backtest["Strategy_Rolling_Sharpe"] = (strategy_excess.rolling(window=rolling_window).mean() / strategy_excess.rolling(window=rolling_window).std()) * np.sqrt(annual_trading_days)
backtest["Buy_Hold_Rolling_Sharpe"] = (buy_hold_excess.rolling(window=rolling_window).mean() / buy_hold_excess.rolling(window=rolling_window).std()) * np.sqrt(annual_trading_days)

# Calculate drawdowns
backtest["Strategy_Cum_Max"] = backtest["Account_Value"].cummax()
backtest["Buy_Hold_Cum_Max"] = backtest["Buy_and_Hold_Account_Value"].cummax()
backtest["Strategy_Drawdown"] = (backtest["Account_Value"] - backtest["Strategy_Cum_Max"]) / backtest["Strategy_Cum_Max"]
backtest["Buy_Hold_Drawdown"] = (backtest["Buy_and_Hold_Account_Value"] - backtest["Buy_Hold_Cum_Max"]) / backtest["Buy_Hold_Cum_Max"]

# Reset index
backtest_reset = backtest.reset_index()

# Export results to csv for Power BI
save_path = "../results/backtest_results.csv"
backtest_reset.to_csv(save_path, index=False)
print(f"\n Data saved successfully to {save_path}")