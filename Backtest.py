import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web

plt.style.use("dark_background")
ma1 = 30
ma2 = 100

start = dt.datetime.now() - dt.timedelta(days = 365 * 5)
end = dt.datetime.now()

data = web.DataReader('GLD', 'yahoo', start, end)
data[f'SMA_{ma1}'] = data['Adj Close'].rolling(window=ma1).mean()
data[f'SMA_{ma2}'] = data['Adj Close'].rolling(window=ma2).mean()

data = data.iloc[ma2:]

plt.plot(data['Adj Close'], label = "Gold Price",color ="green")
plt.plot(data[f'SMA_{ma1}'], label = f"SMA_{ma1}",color = "red")
plt.plot(data[f'SMA_{ma2}'], label = f"SMA_{ma2}",color = "blue")
plt.legend(loc = "upper left")


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

data['Buy Signals'] = buysignals
data['Sell Signals'] = sellsignals

print(data)

plt.plot(data['Adj Close'], label = "Gold Price",color ="white")
plt.plot(data[f'SMA_{ma1}'], label = f"SMA_{ma1}",color = "purple", linestyle= "--")
plt.plot(data[f'SMA_{ma2}'], label = f"SMA_{ma2}",color = "yellow", linestyle= "--")
plt.scatter(data.index, data['Buy Signals'], label="Buy Signal", marker = "^", color= "green", lw= 3)
plt.scatter(data.index, data['Sell Signals'], label="Sell Signal", marker = "v", color= "red", lw= 3 )
plt.legend(loc="upper left")
plt.show()