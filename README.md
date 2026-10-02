ASX Market Analyzer

Simple Python tool for analysing ASX stocks with yfinance.

Features

Multiple ASX tickers

Custom period and interval

## Data Options

Periods: `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

Intervals:
- `1m` → up to 8 days
- `2m–90m` → up to 60 days
- `1h / 60m` → up to 730 days
- `1d+` → long-term history

`Period` = total history range  
`Interval` = size of each candle

Excel export

Run:

python main.py

Example input: BHP,CBA,WES

For educational and personal research purposes only.