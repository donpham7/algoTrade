# Raw Package
import numpy as np
import pandas as pd
import csv
import json
import time

# Data Source
import yfinance as yf

globalId = 0


class user:
    """
    User Class is the class that stores the information for the trader
    """

    def __init__(self, id=globalId, currentAmount=10000, stocks={}, purchaseHistory=[]):
        """
        __init__ Creates new User Class

        Args:
            id (_type_, optional): Defaults to globalId.
            currentAmount (int, optional): Defaults to 10000.
            stocks (dict, optional): Defaults to {}.
            purchaseHistory (list, optional): Defaults to [].
        """
        global globalId
        self.id = id
        self.currentAmount = currentAmount
        self.stocks = stocks
        self.purchaseHistory = purchaseHistory
        if id == globalId:
            globalId += 1

    def __str__(self) -> str:
        """
        __str__ string format of User

        Returns:
            str: string format of User
        """
        seperator = "*-----------------------SUMMARY------------------------*"
        userStr = "User ID: {id}\n".format(id=self.id)
        currentAmount = "Current Amount in USD: {currentAmount}\n".format(
            currentAmount=self.currentAmount
        )
        currentStockString = ""
        for stock in self.stocks.keys():
            tempString = stock + ": " + str(self.stocks[stock]) + "\n"
            currentStockString += tempString
        return (
            "\n"
            + seperator
            + "\n"
            + userStr
            + currentAmount
            + currentStockString
            + seperator
            + "\n"
        )

    def buyStock(self, ticker: str):
        """
        buyStock User buy stock function

        Args:
            ticker (str): Ticker symbol of a stock (ie. AAPL, MSFT, TMUS, etc.)

        Returns:
            _type_: -1 on ERROR, 0 on SUCCESS
        """
        data = yf.download(tickers=ticker, period="1d", interval="1m")
        if data.empty:
            print("ERROR: Stock not found\n")
            return -1
        else:
            price = float(data["Open"].iloc[-1])
            shareCount = input(
                "How many do you want to buy? ({} max)\n".format(
                    int(self.currentAmount // price)
                )
            )
            try:
                shareCount = float(shareCount)
            except:
                print("ERROR: Amount of shares must be numeric\n")
                return -1
        if shareCount > 0:
            if float(shareCount) * price < self.currentAmount:
                print("Buying", shareCount, "shares of", ticker, "for", price, "each")
                self.currentAmount -= float(shareCount) * price
                if ticker not in self.stocks:
                    self.stocks[ticker] = int(shareCount)
                else:
                    self.stocks[ticker] += int(shareCount)
                self.purchaseHistory.append(
                    transaction(
                        True, ticker, int(shareCount), price * float(shareCount), price
                    )
                )
            else:
                print("ERROR: Insufficient Funds\n")
                return -1
        else:
            print("ERROR: Amount of shares must be positive\n")
            return -1
        return 0

    def sellStock(self, ticker: str):
        """
        sellStock User sell stock functon

        Args:
            ticker (str): Ticker symbol of a stock (ie. AAPL, MSFT, TMUS, etc.)

        Returns:
            _type_: -1 on ERROR, 0 on SUCCESS
        """
        if ticker in self.stocks:
            shareCount = input(
                "How many do you want to sell? ({} max)\n".format(
                    int(self.stocks[ticker])
                )
            )
            try:
                shareCount = float(shareCount)
            except:
                print("ERROR: Amount of shares must be numeric\n")
                return -1
        else:
            print("ERROR: Stock not in possession\n")
            return -1
        if int(shareCount) < 0:
            print("ERROR: Amount of shares must be positive\n")
            return -1
        data = yf.download(tickers=ticker, period="1d", interval="1m")
        price = float(data["Open"].iloc[-1])
        if int(shareCount) > self.stocks[ticker]:
            sellMax = input(
                "WARNING: Attempting to sell more shares than owned. Sell max instead? ({max} shares)".format(
                    max=self.stocks[ticker]
                )
            )
            if sellMax:
                del self.stocks[ticker]
                self.currentAmount += price * float(shareCount)
                self.purchaseHistory.append(
                    transaction(
                        False,
                        ticker,
                        shareCount,
                        price * float(shareCount),
                        price,
                        shareCount,
                    )
                )

        elif int(shareCount) == self.stocks[ticker]:
            del self.stocks[ticker]
            self.currentAmount += price * float(shareCount)
            self.purchaseHistory.append(
                transaction(False, ticker, shareCount, price * float(shareCount), price)
            )

        else:
            print(self.stocks[ticker])
            self.stocks[ticker] -= int(shareCount)
            self.currentAmount += price * float(shareCount)
            self.purchaseHistory.append(
                transaction(False, ticker, shareCount, price * float(shareCount), price)
            )

        print("Selling", shareCount, "shares of", ticker, "for", price, "each")
        return 0

    def saveTransactionHistory(self):
        """
        saveTransactionHistory Saves transaction history to a CSV file transactionHistory.csv in data folder
        """
        with open("../data/transactionHistory.csv", "a") as csv_file:
            wr = csv.writer(csv_file, delimiter=",")
            for transaction in self.purchaseHistory:
                wr.writerow(
                    [
                        transaction.transactionId,
                        transaction.isBuy,
                        transaction.stockTicker,
                        transaction.shares,
                        transaction.dollarAmount,
                        transaction.dollarsPerShare,
                    ]
                )
            self.purchaseHistory = []

    def saveUser(self):
        """
        saveUser Saves user information to data folder via userProfile.csv and stock.json
        """
        with open("../data/userProfile.csv", "w") as csv_file:
            wr = csv.writer(csv_file, delimiter=",")
            wr.writerow([self.id, self.currentAmount])
        with open("../data/stocks.json", "w") as json_file:
            stockJson = json.dumps(self.stocks)
            json_file.write(stockJson)

    def savePortfolio(self):
        """
        savePortfolio saves Portfolio value to portfolioHistory.csv
        """
        with open("../data/portfolioHistory.csv", "a") as csv_file:
            wr = csv.writer(csv_file, delimiter=",")
            wr.writerow([time.time(), self.currentAmount])

    def reset(self):
        """
        reset Resets User to default values (Not including ID)
        """
        self.currentAmount = 10000.00
        self.stocks = {}
        self.purchaseHistory = []
        with open("../data/transactionHistory.csv", "w") as csv_file:
            wr = csv.writer(csv_file, delimiter=",")
        with open("../data/portfolioHistory.csv", "w") as csv_file:
            wr = csv.writer(csv_file, delimiter=",")


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


# Start Script
if __name__ == "__main__":
    # try:
    with open("../data/userProfile.csv", "r") as csv_file:
        wr = csv.reader(csv_file, delimiter=",")
        for line in wr:
            id = int(line[0])
            currentAmount = float(line[1])
    with open("../data/stocks.json", "r") as json_file:
        stocks = json.load(json_file)
    superUser = user(id, currentAmount, stocks)

    saveTime = time.time()

    while True:
        if time.time() - saveTime >= 60:
            saveTime = time.time()
            print("AUTOSAVING...")
            superUser.saveTransactionHistory()
            superUser.saveUser()
            superUser.savePortfolio()
            print("SAVED")

        cmd = input("Buy (b), Sell (s), View Portfolio(v) or Other(o)?\nType Command: ")
        match cmd:
            case "b":
                ticker = input("What stock do you want to buy?\n").upper()
                superUser.buyStock(ticker)

            case "s":
                print(*superUser.stocks.keys(), sep="\n")
                ticker = input("What stock do you want to sell?\n").upper()
                superUser.sellStock(ticker)

            case "v":
                print(superUser)
            case "o":
                cmd = input("Save History(s) or Reset User(r)?\n")
                match cmd:
                    case "s":
                        superUser.saveTransactionHistory()
                        superUser.saveUser()
                    case "r":
                        superUser.reset()

            case _:
                print("ERROR: Invalid command\n")
