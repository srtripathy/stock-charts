"""Entry point for the stock-charts CLI."""

import argparse
import sys


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="stock-charts",
        description="Fetch and display stock charts from the command line.",
    )
    parser.add_argument("ticker", help="Stock ticker symbol (e.g. AAPL)")
    parser.add_argument(
        "--period",
        default="1mo",
        choices=["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
        help="Time period to display (default: 1mo)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    print(f"Fetching chart for {args.ticker} over {args.period}...")
    # TODO: implement chart fetching and rendering
    return 0


if __name__ == "__main__":
    sys.exit(main())
