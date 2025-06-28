"""Simple Binance order execution wrapper."""
import logging
import time
from typing import Dict, Optional

try:
    import requests
except Exception:  # pragma: no cover - optional dependency
    requests = None

from ..config import config

logger = logging.getLogger(__name__)

API_URL = "https://api.binance.com/api/v3/order"


class BinanceExecution:
    """Place orders on Binance with optional paper trading."""

    def __init__(self, live: Optional[bool] = None) -> None:
        cfg = config.get("binance", {})
        self.live = live if live is not None else cfg.get("live", False)
        self.api_key = cfg.get("api_key", "")
        self.api_secret = cfg.get("api_secret", "")
        self.max_position = float(cfg.get("max_position", 0))
        self.rate_limit = float(cfg.get("rate_limit", 1))
        self._last_call = 0.0

    def _throttle(self) -> None:
        wait = self.rate_limit - (time.time() - self._last_call)
        if wait > 0:
            time.sleep(wait)
        self._last_call = time.time()

    def place_order(
        self,
        symbol: str,
        side: str,
        quantity: float,
        stop_loss: Optional[float] = None,
    ) -> Dict:
        """Place a market order or log it when paper trading."""
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        if self.max_position and quantity > self.max_position:
            raise ValueError("quantity exceeds max position")
        if stop_loss is not None and stop_loss <= 0:
            raise ValueError("stop_loss must be positive")

        if not self.live:
            logger.info("Paper order %s %s %s", side, quantity, symbol)
            return {
                "symbol": symbol,
                "side": side,
                "quantity": quantity,
                "paper": True,
            }

        if not requests:
            logger.warning("requests module not available, cannot place order")
            return {}

        self._throttle()
        headers = {"X-MBX-APIKEY": self.api_key} if self.api_key else {}
        payload = {
            "symbol": symbol,
            "side": side.upper(),
            "type": "MARKET",
            "quantity": quantity,
        }
        if stop_loss:
            payload["stopPrice"] = stop_loss
            payload["type"] = "STOP_LOSS_MARKET"

        try:
            resp = requests.post(API_URL, headers=headers, data=payload, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:  # pragma: no cover - network errors
            logger.error("Order failed: %s", exc)
            raise RuntimeError("order failed") from exc
