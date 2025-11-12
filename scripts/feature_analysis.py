import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

# Pull in trades data and backtest_features data
trade_path = '../results/trades.csv'
features_path = '../results/backtest_features.csv'
trades = pd.read_csv(trade_path)
features = pd.read_csv(features_path)

# Merge to bring in EMA features at the trade entry date
merged = trades.merge(features[["Date", "EMA_Gap_Pct"]], left_on="Entry_Date", right_on="Date", how="left")

# Drop rows with missing EMA gap or Trade_Return Data
merged = merged.dropna(subset=["EMA_Gap_Pct", "Trade_Return"])

# Take absolute value of EMA Gap %
merged["EMA_Gap_Pct"] = merged["EMA_Gap_Pct"].abs()

# 1 Basic summary stats
print("\n--- Summary Statistics ---")
print(merged[["EMA_Gap_Pct", "Trade_Return"]].describe())

# 2 Scatter plot: EMA gap vs trade return
plt.figure(figsize=(8,5))
sns.scatterplot(x="EMA_Gap_Pct", y="Trade_Return", hue="Direction", data=merged, alpha=.6)
plt.title("Trade Return vs EMA Gap % at Entry")
plt.xlabel("EMA Gap % (9EMA - 20EMA) / 20EMA")
plt.ylabel("Trade Return")
plt.legend(title="Trade Direction")
plt.tight_layout()
plt.show()

# 3 Correlation
corr = merged["EMA_Gap_Pct"].corr(merged["Trade_Return"])
print(f"\nCorrelation between EMA_Gap_Pct and Trade_Return: {corr:.3f}")

# 4 Linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(merged["EMA_Gap_Pct"], merged["Trade_Return"])

print("\n--- Linear Regression: Trade_Return ~ EMA_Gap_Pct ---")
print(f"Slope: {slope:.4f}")
print(f"Intercept: {intercept:.4f}")
print(f"rsquared: {r_value**2:.4f}")
print(f"p-value: {p_value:.4f}")