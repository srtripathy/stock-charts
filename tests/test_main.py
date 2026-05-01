"""Tests for the stock_charts CLI."""

from stock_charts.main import parse_args


def test_parse_args_defaults():
    args = parse_args(["AAPL"])
    assert args.ticker == "AAPL"
    assert args.period == "1mo"


def test_parse_args_custom_period():
    args = parse_args(["TSLA", "--period", "1y"])
    assert args.ticker == "TSLA"
    assert args.period == "1y"
