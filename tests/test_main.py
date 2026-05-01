"""Tests for the current fixed JEPI/JEPQ chart script."""

from pathlib import Path


MAIN_PATH = Path(__file__).resolve().parents[1] / "stock_charts" / "main.py"


def _read_main_source() -> str:
    return MAIN_PATH.read_text(encoding="utf-8")


def test_main_uses_fixed_tickers_and_period():
    source = _read_main_source()
    assert 'tickers = ["JEPI", "JEPQ"]' in source
    assert 'period="4y"' in source


def test_main_saves_expected_output_chart():
    source = _read_main_source()
    assert 'plt.savefig("jepi_jepq_normalized.png", dpi=300)' in source


def test_main_reports_dividend_summary():
    source = _read_main_source()
    assert 'Dividend Summary (4Y cumulative):' in source
