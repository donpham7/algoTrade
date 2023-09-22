# Raw Package
import numpy as np
import pandas as pd

#Data Source
import yfinance as yf

# use download to retrieve a dataframe structure of AAPL
data = yf.download("AAPL", period="1d", interval="1m")

# write dataframe to csv, view csv for column labels
data.to_csv("aapl.csv")

# gets list of open prices
openPrices = data["Open"]

# prints index 4 of open prices
print(openPrices.iloc[4]) 