"""Real-time market data via WebSocket connections."""
import json
import logging
import threading
from typing import Callable, Optional

try:
    import websocket  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    websocket = None

logger = logging.getLogger(__name__)


class MarketWebSocket:
    """Connect to an exchange WebSocket and stream updates."""

    def __init__(self, url: str, callback: Callable[[dict], None]) -> None:
        self.url = url
        self.callback = callback
        self._ws: Optional["websocket.WebSocketApp"] = None

    def connect(self) -> None:
        """Start the WebSocket connection in a background thread."""
        if not websocket:
            logger.warning("websocket-client not available")
            return
        self._ws = websocket.WebSocketApp(self.url, on_message=self._on_message)
        thread = threading.Thread(target=self._ws.run_forever, daemon=True)
        thread.start()

    def _on_message(self, ws: object, message: str) -> None:  # pragma: no cover - callback
        try:
            data = json.loads(message)
        except Exception:
            logger.debug("Non-JSON message received")
            return
        self.callback(data)
