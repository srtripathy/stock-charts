# Save as plot_jepi_jepq.py and run: python plot_jepi_jepq.py
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

tickers = ["JEPI", "JEPQ"]
# Download 4 years of history
data = yf.download(tickers, period="4y", progress=False, auto_adjust=True)["Close"]

# If a ticker has no data or is missing, yfinance returns NaNs; drop columns with all NaN
data = data.dropna(axis=1, how="all")

# Align to common dates (inner join)
data = data.dropna(how="any")
data.index = pd.to_datetime(data.index)
if data.index.tz is not None:
    data.index = data.index.tz_localize(None)
data.index = data.index.normalize()

if data.empty:
    raise SystemExit("No overlapping data available for JEPI and JEPQ. Check ticker availability or internet access.")

# Normalize to 100 at first common date
normalized = data.div(data.iloc[0]).mul(100)

# Fetch dividends and convert to cumulative totals over the same time range.
dividend_start = data.index.min()
dividend_end = data.index.max()
dividends = pd.DataFrame(index=data.index)

for ticker in normalized.columns:
    ticker_dividends = yf.Ticker(ticker).dividends
    if ticker_dividends.empty:
        dividends[ticker] = 0.0
        continue

    ticker_dividends.index = pd.to_datetime(ticker_dividends.index)
    if ticker_dividends.index.tz is not None:
        ticker_dividends.index = ticker_dividends.index.tz_localize(None)
    ticker_dividends.index = ticker_dividends.index.normalize()
    ticker_dividends = ticker_dividends.groupby(level=0).sum()
    ticker_dividends = ticker_dividends.loc[
        (ticker_dividends.index >= dividend_start) & (ticker_dividends.index <= dividend_end)
    ]
    dividends[ticker] = ticker_dividends.reindex(data.index, fill_value=0.0).cumsum()

# Plot
plt.style.use("seaborn-v0_8-darkgrid")
fig, (ax_price, ax_div) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
for col in normalized.columns:
    ax_price.plot(normalized.index, normalized[col], label=f"{col} (normalized)")
    ax_price.text(
        normalized.index[-1],
        normalized[col].iloc[-1],
        f"{normalized[col].iloc[-1]:.1f}",
        va="center",
        fontsize=9,
    )
    ax_div.plot(dividends.index, dividends[col], label=f"{col} (cumulative dividends)", linestyle="--")
    ax_div.text(
        dividends.index[-1],
        dividends[col].iloc[-1],
        f"${dividends[col].iloc[-1]:.2f}",
        va="center",
        fontsize=9,
    )

ax_price.set_title("JEPI vs JEPQ — 4Y Price Growth and Dividends")
ax_price.set_ylabel("Normalized index (start = 100)")
ax_price.legend()

ax_div.set_xlabel("Date")
ax_div.set_ylabel("Cumulative dividends ($)")
ax_div.legend()

plt.tight_layout()
plt.savefig("jepi_jepq_normalized.png", dpi=300)
print("Saved chart to jepi_jepq_normalized.png")

# Summary table
summary = pd.DataFrame({
    "start_date": [data.index[0]]*len(data.columns),
    "start_price": data.iloc[0].values,
    "end_date": [data.index[-1]]*len(data.columns),
    "end_price": data.iloc[-1].values,
})
summary["pct_change"] = (summary["end_price"] / summary["start_price"] - 1) * 100
print("\nSummary:")
print(summary.round(2).to_string(index=False))

dividend_summary = pd.DataFrame({
    "ticker": dividends.columns,
    "cumulative_dividends": [dividends[col].iloc[-1] for col in dividends.columns],
})
print("\nDividend Summary (4Y cumulative):")
print(dividend_summary.round(2).to_string(index=False))

