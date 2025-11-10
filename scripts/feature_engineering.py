import pandas as pd

# Load backtest results from performance analysis (already has a lot of calculated values included)
df = pd.read_csv("../results/backtest_results.csv")

# Compute EMA's if they are for some reason not in the backtest results
if "EMA_9" not in df.columns or "EMA_20" not in df.columns:
    df["EMA_9"] = df["Close"].ewm(span=9, adjust=False).mean()
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()

# Calculate EMA gap
df['EMA_Gap'] = df["EMA_9"] - df["EMA_20"]

# Calculate EMA gap percentage
df["EMA_Gap_Pct"] = (df["EMA_9"] - df["EMA_20"]) / df["EMA_20"]

# Quick sanity check
print(df[["Date", "EMA_9", "EMA_20", "EMA_Gap", "EMA_Gap_Pct"]].tail())

# Save the new features set
save_path = "../results/backtest_features.csv"
df.to_csv(save_path, index=False)

print(f"Feature engineering complete! Saved to {save_path}")
print("Columns added: EMA_Gap and EMA_Gap_Pct")