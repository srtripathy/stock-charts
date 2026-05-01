# Stock Charts

A CLI application for fetching and displaying stock charts.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
stock-charts AAPL
stock-charts TSLA --period 1y
```

## Development

Run tests:

```bash
pytest
```
