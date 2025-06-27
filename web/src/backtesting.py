"""Simple historical data backtesting utilities."""
try:
    import pandas as pd  # type: ignore
    _HAS_PANDAS = True
except Exception:  # pragma: no cover - pandas optional
    class _DummyFrame:
        pass

    class pd:  # type: ignore
        DataFrame = _DummyFrame

    _HAS_PANDAS = False
from typing import Callable, List


def load_prices(csv_path: str) -> pd.DataFrame:
    """Load historical price data from CSV."""
    if not _HAS_PANDAS:
        raise RuntimeError('pandas not available')
    return pd.read_csv(csv_path, parse_dates=['date'])


def run_backtest(prices: pd.DataFrame, strategy: Callable[[pd.DataFrame], List[int]]) -> float:
    """Run a naive backtest given price data and a strategy callback.

    The strategy should return a list of indexes representing buy signals.
    This placeholder returns cumulative returns for demonstration.
    """
    buy_points = strategy(prices)
    if not buy_points:
        return 0.0
    if not _HAS_PANDAS:
        raise RuntimeError('pandas not available')
    pct_change = prices['close'].pct_change().fillna(0)
    returns = pct_change.iloc[buy_points].sum()
    return float(returns)
