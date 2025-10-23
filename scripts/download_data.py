import os
import yfinance as yf

# Yahoofinance download inputs
ticker = "SPY"
start_date = "1995-10-16"
end_date = "2025-10-21"
interval = "1d"

# Download data from Yahoofinance and polish DataFrame
data = yf.download(ticker, start=start_date, end=end_date, interval=interval, auto_adjust=True)
data.columns = data.columns.droplevel(1)
data.columns.name = None
data.reset_index(inplace=True)

# Ensure data folder exists
os.makedirs("../data", exist_ok=True)

save_path = "../data/spy_daily.csv"

# Save the data in a CSV file
data.to_csv(save_path, index=False)

print(f"\n Data saved successfully to {save_path}")