# Raw Package
import numpy as np
import pandas as pd
import csv

#Data Source
import yfinance as yf

id = 0
class user:
  def __init__(self) -> None:
    global id
    self.id = id
    self.currentAmount = 10000.00
    self.stocks = {}
    self.purchaseHistory = []
    id += 1

  def __str__(self) -> str:
    seperator = "*-----------------------SUMMARY------------------------*"
    userStr = "User ID: {id}\n".format(id = self.id)
    currentAmount = "Current Amount in USD: {currentAmount}\n".format(currentAmount = self.currentAmount)
    currentStockString = ""
    for stock in self.stocks.keys():
      tempString = stock + ": " + str(self.stocks[stock]) + '\n'
      currentStockString += tempString
    return "\n" + seperator + "\n" + userStr + currentAmount + currentStockString + seperator + "\n"
    
  def buyStock(self, ticker: str, amountOfShares: int, price: float):
    if float(amountOfShares) * price < self.currentAmount:
      print("Buying", amountOfShares, "shares of", ticker, "for", price, "each")
      self.currentAmount -= float(amountOfShares) * price
      if ticker not in self.stocks:
        self.stocks[ticker] = int(amountOfShares)
      else:
        self.stocks[ticker] += int(amountOfShares)
      self.purchaseHistory.append(transaction(True, ticker, amountOfShares, price * float(amountOfShares), price))
    else:
      print("ERROR: Insufficient Funds\n")

  def sellStock(self, ticker: str, amountOfShares: int):
    data = yf.download(tickers=ticker, period='1d', interval='1m')
    price = float(data["Open"].iloc[-1])
    if int(amountOfShares) > self.stocks[ticker]:
      sellMax = input("WARNING: Attempting to sell more shares than owned. Sell max instead? ({max} shares)".format(max = self.stocks[ticker]))
      if sellMax:
        del self.stocks[ticker]
        self.currentAmount += price * float(amountOfShares)
        self.purchaseHistory.append(transaction(False, ticker, amountOfShares, price * float(amountOfShares), price))

    elif int(amountOfShares) == self.stocks[ticker]:
      del self.stocks[ticker]
      self.currentAmount += price * float(amountOfShares)
      self.purchaseHistory.append(transaction(False, ticker, amountOfShares, price * float(amountOfShares), price))

    else:
      print(self.stocks[ticker])
      self.stocks[ticker] -= int(amountOfShares)
      self.currentAmount += price * float(amountOfShares)
      self.purchaseHistory.append(transaction(False, ticker, amountOfShares, price * float(amountOfShares), price))

    print("Selling", amountOfShares, "shares of", ticker, "for", price, "each")

  def saveTransactionHistory(self):
    with open("transactionHistory.csv", 'w') as csv_file:
      wr = csv.writer(csv_file, delimiter=',')
      wr.writerow(["TransactionId", "isBuy", "Ticker", "Shares", "Total Amount", "Dollars per Share"])
      for transaction in self.purchaseHistory:
        wr.writerow([transaction.transactionId, transaction.isBuy, transaction.stockTicker, transaction.shares, transaction.dollarAmount, transaction.dollarsPerShare])


transactionId = 0
class transaction:
  def __init__(self, isBuy, stockTicker, shares, dollarAmount, dollarsPerShare) -> None:
    global transactionId
    self.transactionId = transactionId
    transactionId += 1
    self.isBuy = isBuy
    self.stockTicker = stockTicker
    self.shares = shares
    self.dollarAmount = dollarAmount
    self.dollarsPerShare = dollarsPerShare

  def __iter__(self):
    return iter([self.transactionId, self.isBuy, self.stockTicker, self.shares, self.dollarAmount, self.dollarsPerShare])


superUser = user()
while True:
  cmd = input("Buy (b), Sell (s) or Other(o)?\n")
  if cmd == 'b':
    ticker = input("What stock do you want to buy?\n").upper()
    data = yf.download(tickers=ticker, period='1d', interval='1m')
    if data.empty:
      print("ERROR: Stock not found\n")
    else:
      price = float(data["Open"].iloc[-1])
      shareCount = input("How many do you want to buy? ({} max)\n".format(int(superUser.currentAmount // price)))
      superUser.buyStock(ticker, shareCount, price)
  elif cmd == 's':
    print(*superUser.stocks.keys(), sep="\n")
    ticker = input("What stock do you want to sell?\n").upper()
    if ticker in superUser.stocks:
      shareCount = input("How many do you want to sell? ({} max)\n".format(int(superUser.stocks[ticker])))
      superUser.sellStock(ticker, shareCount)
    else:
      print("ERROR: Stock not in possession\n")
  elif cmd == 'o':
    cmd = input("Save Transaction History(s)?\n")
    if cmd == 's':
      superUser.saveTransactionHistory()
    
  else:
    print("ERROR: Invalid command\n")
  
  print(superUser)

