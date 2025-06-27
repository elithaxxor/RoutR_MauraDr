"""Simple historical data backtesting utilities."""
import pandas as pd
from typing import Callable, List


def load_prices(csv_path: str) -> pd.DataFrame:
    """Load historical price data from CSV."""
    return pd.read_csv(csv_path, parse_dates=['date'])


def run_backtest(prices: pd.DataFrame, strategy: Callable[[pd.DataFrame], List[int]]) -> float:
    """Run a naive backtest given price data and a strategy callback.

    The strategy should return a list of indexes representing buy signals.
    This placeholder returns cumulative returns for demonstration.
    """
    buy_points = strategy(prices)
    if not buy_points:
        return 0.0
    pct_change = prices['close'].pct_change().fillna(0)
    returns = pct_change.iloc[buy_points].sum()
    return float(returns)
