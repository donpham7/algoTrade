import yfinance as yf

transactionId = 0


class transaction:
    """
    Transaction Class represents the buy and sell actions
    """

    def __init__(
        self, isBuy, stockTicker, shares, dollarAmount, dollarsPerShare
    ) -> None:
        """
        __init__ Creates a Transaction

        Args:
            isBuy (bool): True if transaction was a purchase else False
            stockTicker (_type_): Ticker symbol of a stock (ie. AAPL, MSFT, TMUS, etc.)
            shares (_type_): Amount of Shares bought/sold
            dollarAmount (_type_): Total dollar amount of transaction
            dollarsPerShare (_type_): Dollars per Share at time of transaction
        """
        global transactionId
        self.transactionId = transactionId
        transactionId += 1
        self.isBuy = isBuy
        self.stockTicker = stockTicker
        self.shares = shares
        self.dollarAmount = dollarAmount
        self.dollarsPerShare = dollarsPerShare

    def __iter__(self):
        return iter(
            [
                self.transactionId,
                self.isBuy,
                self.stockTicker,
                self.shares,
                self.dollarAmount,
                self.dollarsPerShare,
            ]
        )
