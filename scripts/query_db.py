import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("../database/backtest.db")

# List of all tables
tables = pd.read_sql_query("SELECT name from sqlite_master WHERE type='table';", conn)
print("Tables in database", tables)

# Peek at historical price data
price_preview = pd.read_sql_query("SELECT * FROM historical_price_data LIMIT 5;", conn)
print("historical price data first 5 rows")
print(price_preview)

# Peek at backtesting results
results_preview = pd.read_sql_query("SELECT * FROM strategy_results LIMIT 5;", conn)
print("historical price data first 5 rows")
print(results_preview)

# Close the connection
conn.close()