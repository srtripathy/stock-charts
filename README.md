# Stock Charts

A fixed script that downloads and plots 4-year performance data for JEPI and JEPQ.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pip install yfinance pandas matplotlib
```

## Usage

```bash
python -m stock_charts.main
```

This generates:

- `jepi_jepq_normalized.png` with normalized price growth (start = 100) and cumulative dividends over 4 years
- Console summaries for price change and cumulative dividends

## Development

Run tests:

```bash
python -m pytest
```
