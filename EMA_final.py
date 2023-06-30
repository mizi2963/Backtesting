import pandas as pd
import yfinance as yf
import math

#input data
#stock = input("Enter the symbol of the stock: ")
#period = input("Enter the time period: ")
#interval = input("Enter the trading interval: ")
span = int(input("Span for calculating EMA is = "))

closing_prices = (yf.download(tickers = "MSFT",        # list of tickers
            period = "5y",                             # time period
            interval = "1d",                           # trading interval
            prepost = False,                           # download pre/post market hours data?
            repair = True))["Close"]                   # repair obvious price errors e.g. 100x?

# Create a pandas Series with the EMA values
ema_series = pd.Series((closing_prices.ewm(span = span, adjust=False).mean()), index=closing_prices.index)

# Create a dataframe to store trade data
trades = pd.DataFrame(columns=["Buy_date","Buy_price","Sell_date","Sell_price","Position"])

# Perform backtest
flag = False
a = 0
found_buy = 0
found_sell = 0

for i in range(span, len(closing_prices)):
    if closing_prices[i] > ema_series[i] and flag == False:
        trades.loc[a, "Buy_date"] = closing_prices.index[i]
        trades.loc[a, "Buy_price"] = closing_prices[i]
        flag = True
        found_buy = 1
    if closing_prices[i] < ema_series[i] and flag == True:
        trades.loc[a, "Sell_date"] = closing_prices.index[i]
        trades.loc[a, "Sell_price"] = closing_prices[i]
        flag = False
        found_sell = 1
    if (found_buy==1 and found_sell==1):
        trades.loc[i]["Position"] = trades.loc[i]["Sell_price"] - trades.loc[i]["Buy_price"]
        a = a+1
        found_buy=0
        found_sell=0

win = 0
loss = 0

for i in range(0,len(trades)):
   if trades.loc[i]["Position"]>0:
       win = win +1
   else:
       loss = loss+1

print(trades)
print("The overall profit/loss is",trades['Position'].sum())
print("The win probability is", win/(len(trades)-1)*100,"%")

