import pandas as pd

csv_file = "../data/spy_daily.csv"

data = pd.read_csv(csv_file, parse_dates=["Date"])

data.set_index("Date", inplace=True)

data.sort_index(inplace=True)
