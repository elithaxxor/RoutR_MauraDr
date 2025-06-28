import unittest

from web.src.portfolio import Portfolio


class TestPortfolio(unittest.TestCase):
    def test_update_existing_position(self):
        pf = Portfolio()
        pf.update("AAPL", 1, 10.0)
        pf.update("AAPL", 1, 12.0)
        pos = pf.positions["AAPL"]
        self.assertEqual(pos.quantity, 2)
        self.assertAlmostEqual(pos.cost_basis, 11.0)

    def test_value(self):
        pf = Portfolio()
        pf.update("AAPL", 2, 10.0)
        pf.update("MSFT", 1, 20.0)
        prices = {"AAPL": 15.0, "MSFT": 30.0}
        self.assertAlmostEqual(pf.value(prices), 2 * 15.0 + 1 * 30.0)


if __name__ == "__main__":
    unittest.main()

