import unittest
from unittest import mock

from web.src.trading.binance_execution import BinanceExecution


class TestBinanceExecution(unittest.TestCase):
    def setUp(self):
        self.cfg_patch = mock.patch(
            "web.src.trading.binance_execution.config",
            {
                "binance": {
                    "api_key": "key",
                    "api_secret": "secret",
                    "live": False,
                    "max_position": 2,
                    "rate_limit": 0,
                }
            },
        )
        self.cfg_patch.start()

    def tearDown(self):
        self.cfg_patch.stop()

    def test_paper_order(self):
        be = BinanceExecution()
        result = be.place_order("BTCUSDT", "BUY", 1)
        self.assertTrue(result["paper"])
        self.assertEqual(result["quantity"], 1)

    def test_live_order(self):
        requests_mock = mock.Mock()
        requests_mock.post.return_value.json.return_value = {"status": "filled"}
        requests_mock.post.return_value.raise_for_status.return_value = None
        with mock.patch(
            "web.src.trading.binance_execution.requests", requests_mock
        ):
            cfg = {
                "binance": {
                    "api_key": "k",
                    "api_secret": "s",
                    "live": True,
                    "max_position": 5,
                    "rate_limit": 0,
                }
            }
            with mock.patch(
                "web.src.trading.binance_execution.config", cfg
            ):
                be = BinanceExecution()
                res = be.place_order("ETHUSDT", "SELL", 1.5, stop_loss=1.0)
        requests_mock.post.assert_called_once()
        self.assertEqual(res["status"], "filled")

    def test_max_position(self):
        be = BinanceExecution()
        with self.assertRaises(ValueError):
            be.place_order("BTCUSDT", "BUY", 3)


if __name__ == "__main__":
    unittest.main()
