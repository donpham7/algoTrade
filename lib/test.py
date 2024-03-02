import unittest
from unittest.mock import patch
import main
import yfinance as yf


class tradingFunctionTest(unittest.TestCase):
    user = main.user()

    def setUp(self) -> None:
        self.assertEqual(self.user.currentAmount, 10000)
        self.assertEqual(self.user.id, 0)
        self.assertEqual(self.user.purchaseHistory, [], self.user.purchaseHistory)
        self.assertEqual(self.user.stocks, {})
        self.assertEqual(main.globalId, 1)

    def tearDown(self) -> None:
        self.user.currentAmount = 10000
        self.user.purchaseHistory = []
        self.user.stocks = {}
        self.assertEqual(self.user.currentAmount, 10000)
        self.assertEqual(self.user.id, 0)
        self.assertEqual(self.user.purchaseHistory, [])
        self.assertEqual(self.user.stocks, {})

    def test_buyShares(self):
        ticker = "AAPL"
        data = float(
            yf.download(tickers=ticker, period="1d", interval="1m")["Open"].iloc[-1]
        )
        buyShares = self.user.currentAmount // data
        with patch("builtins.input", return_value=buyShares):
            self.assertEqual(self.user.buyStock("AAPL"), 0)
        self.assertEqual(self.user.stocks["AAPL"], buyShares)

    @unittest.expectedFailure
    def test_buySharesNegative(self):
        ticker = "AAPL"
        buyShares = -1
        with patch("builtins.input", return_value=buyShares):
            self.assertEqual(self.user.buyStock("AAPL"), -1)
        self.assertEqual(self.user.stocks["AAPL"], buyShares)

    @unittest.expectedFailure
    def test_failBuyShares(self):
        # Calculate STOCK Price
        ticker = "AAPL"
        data = float(
            yf.download(tickers=ticker, period="1d", interval="1m")["Open"].iloc[-1]
        )

        buyShares = self.user.currentAmount // data + 1
        with patch("builtins.input", return_value=buyShares):
            self.assertEqual(self.user.buyStock(ticker), -1)
        self.assertEqual(self.user.stocks[ticker], buyShares)

    # Buy 3 Shares and Sell 2, Net 1
    def test_sellShares(self):
        buyShares = 3
        sellShares = 2
        ticker = "AAPL"
        with patch("builtins.input", return_value=buyShares):
            self.assertEqual(self.user.buyStock(ticker), 0)
            self.assertEqual(self.user.stocks[ticker], 3)

        with patch("builtins.input", return_value=sellShares):
            self.assertEqual(self.user.sellStock(ticker), 0)
        self.assertEqual(self.user.stocks[ticker], 1)

    # Buy 3 Shares and Sell 4, error
    @unittest.expectedFailure
    def test_sellSharesOverMax(self):
        buyShares = 3
        sellShares = 4
        ticker = "AAPL"
        with patch("builtins.input", return_value=buyShares):
            self.assertEqual(self.user.buyStock(ticker), 0)
            self.assertEqual(self.user.stocks[ticker], 3)

        with patch("builtins.input", return_value=sellShares):
            self.assertEqual(self.user.sellStock(ticker), -1)
        self.assertEqual(self.user.stocks[ticker], -1)

    # Buy 3 Shares and Sell Negative, error
    @unittest.expectedFailure
    def test_sellSharesNegative(self):
        buyShares = 3
        sellShares = -1
        ticker = "AAPL"
        with patch("builtins.input", return_value=buyShares):
            self.assertEqual(self.user.buyStock(ticker), 0)
            self.assertEqual(self.user.stocks[ticker], 3)

        with patch("builtins.input", return_value=sellShares):
            self.assertEqual(self.user.sellStock(ticker), -1)
        self.assertEqual(self.user.stocks[ticker], -1)


if __name__ == "__main__":
    unittest.main()
