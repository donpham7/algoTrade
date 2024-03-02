# Raw Package
import numpy as np
import pandas as pd
import csv
import json
import time
from user import user
from transaction import transaction

# Data Source
import yfinance as yf

# Start Script
if __name__ == "__main__":
    try:
        with open("../data/userProfile.csv", "r") as csv_file:
            wr = csv.reader(csv_file, delimiter=",")
            for line in wr:
                id = int(line[0])
                currentAmount = float(line[1])
        with open("../data/stocks.json", "r") as json_file:
            stocks = json.load(json_file)
        superUser = user(id, currentAmount, stocks)
    except:
        superUser = user()

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
