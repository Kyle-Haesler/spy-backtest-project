import pandas as pd 
import math
from load_data import load_spy_data

# Get SPY daily data
df = load_spy_data()

# Calculate EMAs
df["EMA_9"] = df["Close"].ewm(span=9, adjust=False, min_periods=9).mean()
df["EMA_20"] = df["Close"].ewm(span=20, adjust=False, min_periods=20).mean()

# Add long signal column
df["Long_Signal"] = (
    (df["Close"].shift(1) < df["EMA_9"].shift(1)) &
    (df["EMA_9"] > df["EMA_20"]) &
    (df["Close"] > df["EMA_9"])
).astype(int)

# Add short signal column
df["Short_Signal"] = (
    (df["Close"].shift(1) > df["EMA_9"].shift(1)) &
    (df["EMA_9"] < df["EMA_20"]) &
    (df["Close"] < df["EMA_9"])
).astype(int)

# Run backtest
account_value = 100000
risk_per_trade = .01
in_position = False
trades = []
target_multiplier = 2
df["Account_Value"] = float(account_value)
# Begin plot for buy and hold strategy
buy_and_hold_shares = math.floor(account_value / df.iloc[0].Close)
df["Buy_and_Hold_Account_Value"] = buy_and_hold_shares * df.iloc[0].Close

for i in range(1, len(df)):
    # Get previous and current rows
    prev_row = df.iloc[i-1]
    current_row = df.iloc[i]
    # Plot market value
    df.at[current_row.name, "Buy_and_Hold_Account_Value"] = buy_and_hold_shares * current_row["Close"]   
    # By default, carry forward the previous day's account value
    df.at[current_row.name, "Account_Value"] = df.at[prev_row.name,"Account_Value"]
    # Check to see if we are in a position or not
    if not in_position:
        # Long entry
        if prev_row["Long_Signal"]:
            entry_price = current_row["Open"]
            stop_loss = prev_row["Low"]
            risk = entry_price - stop_loss
            # Handle gap down
            if risk <= 0:
                continue
            shares = math.floor((account_value * risk_per_trade) / max(risk, .01))
            target = entry_price + (target_multiplier * risk)
            # Add trade to list
            in_position = True
            trade = {
                "Entry_Date": current_row.name,
                "Direction": "Long",
                "Shares": shares,
                "Entry_Price": entry_price,
                "Stop_Loss": stop_loss,
                "Target": target
            }
            trades.append(trade)
        # Short entry
        elif prev_row["Short_Signal"]:
            entry_price = current_row["Open"]
            stop_loss = prev_row["High"]
            risk = stop_loss - entry_price
            # Handle gap up
            if risk <= 0:
                continue
            shares = math.floor((account_value * risk_per_trade) / max(risk,.01))
            target = entry_price - (target_multiplier * risk)
            # Add trade to list
            in_position = True
            trade = {
                "Entry_Date": current_row.name,
                "Direction": "Short",
                "Shares": shares,
                "Entry_Price": entry_price,
                "Stop_Loss": stop_loss,
                "Target": target
            }
            trades.append(trade)
    # We are in a position
    else:
        current_trade = trades[-1]
        exit_trade = False
        if current_trade["Direction"] == "Long":
            # Check to see if stop loss or target was hit
            if current_row["Low"] <= current_trade["Stop_Loss"]:
                # Exit for loss :/
                current_trade["Exit_Date"] = current_row.name
                current_trade["Exit_Price"] = current_trade["Stop_Loss"]
                exit_trade = True
            elif current_row["High"] >= current_trade["Target"]:
                # Exit for gain :)
                current_trade["Exit_Date"] = current_row.name
                current_trade["Exit_Price"] = current_trade["Target"]
                exit_trade = True
        elif current_trade["Direction"] == "Short":
            # Check to see if stop loss or target was hit
            if current_row["High"] >= current_trade["Stop_Loss"]:
                # Exit for loss :/
                current_trade["Exit_Date"] = current_row.name
                current_trade["Exit_Price"] = current_trade["Stop_Loss"]
                exit_trade = True
            elif current_row["Low"] <= current_trade["Target"]:
                # Exit for gain :)
                current_trade["Exit_Date"] = current_row.name
                current_trade["Exit_Price"] = current_trade["Target"]
                exit_trade = True
        if exit_trade:
            # Calculate return based on full account
            if current_trade["Direction"] == "Long":
                trade_return = (current_trade["Exit_Price"] - current_trade["Entry_Price"]) * current_trade["Shares"]
            else:
                trade_return = (current_trade["Entry_Price"] - current_trade["Exit_Price"]) * current_trade["Shares"]
            account_value += trade_return
            trade["Trade_Return"] = trade_return
            # Update the DataFrame with new account value
            df.at[current_row.name, "Account_Value"] = account_value
            current_trade["Account_Value"] = account_value
            in_position = False

# Convert trades list to DataFrame
trades_df = pd.DataFrame(trades)

# Calculate trade return
trades_df["Trade_Return"] = trades_df.apply(
    lambda row: (row["Exit_Price"] - row["Entry_Price"]) / row["Entry_Price"]
    if row["Direction"] == "Long"
    else (row["Entry_Price"] - row["Exit_Price"]) / row["Entry_Price"],
    axis=1
)

# Add in column that lets us know result
trades_df["Trade_Result"] = trades_df["Trade_Return"].apply(lambda x: "Win" if x > 0 else "Loss")

# Save path
save_path = "../results/trades.csv"
trades_df.to_csv(save_path, index=False)

print(f" trades level dataset saved to {save_path}")
print(trades_df.head())

