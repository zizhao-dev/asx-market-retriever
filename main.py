import yfinance as yf
import pandas as pd


print("""
ASX Market Analyzer

Available periods:
1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

Available intervals:
1m              → up to 8 days
2m / 5m / 15m
30m / 90m       → up to 60 days
60m / 1h        → up to 730 days
1d / 5d
1wk / 1mo / 3mo → long-term history

Period   = how far back to retrieve
Interval = size of each price candle
""")

period = input("Enter period (e.g. 60d, 1y, 5y, max): ").strip() or "60d"
interval = input("Enter interval (e.g. 5m, 1h, 1d, 1wk, 1mo): ").strip() or "5m"


def get_price_history(ticker):
    stock = yf.Ticker(ticker)

    data = stock.history(
        period=period,
        interval=interval
    )

    return data


tickers_input = input("Enter ASX tickers, separated by commas: ")
tickers = tickers_input.split(",")

intraday_intervals = [
    "1m", "2m", "5m", "15m",
    "30m", "60m", "90m", "1h", "4h"
]

is_intraday = interval in intraday_intervals


for ticker in tickers:
    ticker = ticker.strip().upper()

    if not ticker.endswith(".AX"):
        ticker = ticker + ".AX"

    print(f"\nProcessing {ticker}...")

    history = get_price_history(ticker)

    if history.empty:
        print(f"No data found for {ticker}. Skipping.")
        continue

    if history.index.tz is not None:
        history.index = history.index.tz_localize(None)

    daily_rows = []

    for date, group in history.groupby(history.index.date):
        open_price = group["Open"].iloc[0]
        high_price = group["High"].max()
        low_price = group["Low"].min()
        close_price = group["Close"].iloc[-1]
        volume = group["Volume"].sum()

        row = {
            "Date": date,
            "Open": round(open_price, 2),
            "High": round(high_price, 2),
            "Low": round(low_price, 2),
            "Close": round(close_price, 2),
            "Volume": volume
        }

        if is_intraday:
            high_time = group["High"].idxmax()
            low_time = group["Low"].idxmin()

            row["High Time"] = high_time.strftime("%H:%M")
            row["Low Time"] = low_time.strftime("%H:%M")

        daily_rows.append(row)

    summary_df = pd.DataFrame(daily_rows)

    if is_intraday:
        summary_df = summary_df[
            [
                "Date",
                "Open",
                "High Time",
                "High",
                "Low Time",
                "Low",
                "Close",
                "Volume"
            ]
        ]

    filename = f"{ticker}_analysis.xlsx"

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        history.to_excel(
            writer,
            sheet_name=f"{interval} Data"
        )

    print(f"Export successful: {filename}")