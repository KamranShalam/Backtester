import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as pdr

#Eneter stock/curreny symbol here
currency = "GBPUSD=X"
#Enter Moving Averages here
ma1, ma2 = 10, 100
#Enter how far back you would like to test
start = dt.datetime.now() - dt.timedelta(hours = (24 * 365))
end = dt.datetime.now()

plt.style.use("dark_background")
plt.grid(color ="lightgrey", alpha = 0.2)

data = pdr.DataReader(currency, 'yahoo', start, end)
data[f'SMA_{ma1}'] = data['Adj Close'].rolling(window=ma1).mean()
data[f'SMA_{ma2}'] = data['Adj Close'].rolling(window=ma2).mean()

buysignals = []
sellsignals = []
trigger = 0

for x in range (len(data)):
    if data [f'SMA_{ma1}'].iloc[x] > data[f'SMA_{ma2}'].iloc[x] and trigger != 1:
        buysignals.append(data['Adj Close'].iloc[x])
        sellsignals.append(float('nan'))
        trigger = 1
    elif data [f'SMA_{ma1}'].iloc[x] < data[f'SMA_{ma2}'].iloc[x] and trigger != -1:
        sellsignals.append(data['Adj Close'].iloc[x])
        buysignals.append(float('nan'))
        trigger = -1
    else:
        buysignals.append(float('nan'))
        sellsignals.append(float('nan'))

data['Buy'] = buysignals
data['Sell'] = sellsignals

print(data)

plt.plot(data['Adj Close'], label = currency + " Price",color ="white")
plt.plot(data[f'SMA_{ma1}'], label = f"SMA_{ma1}",color = "purple", linestyle= "--")
plt.plot(data[f'SMA_{ma2}'], label = f"SMA_{ma2}",color = "yellow", linestyle= "--")
plt.scatter(data.index, data['Buy'], label="Buy", marker = "^", color= "green", lw= 3)
plt.scatter(data.index, data['Sell'], label="Sell", marker = "v", color= "red", lw= 3 )
plt.legend(loc="upper left")
plt.show()