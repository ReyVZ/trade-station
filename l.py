import os
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn')

def read(filename = 'quotes/' + os.listdir('quotes')[4]):
    data = pd.read_csv(filename, parse_dates=['<DATE>'])
    data.columns = [d[1:-1].lower() for d in data.columns]
    return data

def upgrade(data, n = 9):
    data['sma'] = data.close.rolling(window=n).mean()
    data['dev'] = data.sma - data.close
    return data

def trade(data, n = 9):
    data['type'] = ''
    ingame = False
    for i in range(n + 1, len(data) - 1):
        if data.sma[i-1] >= data.sma[i-2] and ingame is False:
            data.loc[i, 'type'] = 'in'
            ingame = True
        if data.sma[i-1] < data.sma[i-2] and ingame is True:
            data.loc[i, 'type'] = 'out'
            ingame = False
    return data

def deals(data, cash = 10000):
    deal = data[data.type != ''].copy()
    deal['profit'] = deal.close.rolling(window=2).apply(lambda x: (x[1] - x[0]) / x[0], raw=True)
    deal = deal[deal.type == 'out'].loc[:, ['date', 'close', 'profit']]
    print('Profit: ', (cash * deal.profit).sum(), 'Sharp: ', deal.profit.mean() / deal.profit.std())
    return (cash * deal.profit).sum(), deal.profit.mean() / deal.profit.std()

def plot(x, y):
    plt.figure(figsize=(16, 9))
    plt.plot(x, y)
    plt.show()

def main():
    arr = []
    for f in os.listdir('quotes'):
        for n in range(2, 101):
            data = read('quotes/' + f)
            data = upgrade(data, n = n)
            data = trade(data, n = n)
            res, sharp = deals(data)
            arr.append([f.split('_')[0], n, res, sharp])
    return pd.DataFrame(arr, columns=['ticker', 'period', 'profit', 'sharp'])









