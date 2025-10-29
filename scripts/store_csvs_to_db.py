import os
import pandas as pd
import sqlite3

# Ensure database folder exists
os.makedirs("../database", exist_ok=True)

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect("../database/backtest.db")

# Load csv files
historical_price_df = pd.read_csv("../data/spy_daily.csv")
strategy_results_df = pd.read_csv("../results/backtest_results.csv")

# Write to SQL tables
historical_price_df.to_sql("historical_price_data", conn, if_exists="replace", index=False)
strategy_results_df.to_sql("strategy_results", conn, if_exists="replace", index=False)

# Close the connection
conn.close()

print("CSV files written to database/backtest.db successfully")