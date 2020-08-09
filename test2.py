#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 19:49:54 2019

@author: aviz
"""
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn')

#%%
data = pd.read_csv('gkfx_data_1d/GBPUSD_1900-04-29_2019-04-29_quotes_1440.csv',
                   parse_dates=[0], header=None, 
                   names=['date', 'open', 'high', 'low', 'close', 'vol'])
data = data[data.vol!=0]

for _ in [5, 20, 50, 100]:
    col_name = 'sma' + str(_)
    data[col_name] = data.close.rolling(window=_).mean()
    del col_name

k = 10
data['stoch'] = (data.close - data.low.rolling(window=k).min()) / \
    (data.high.rolling(window=k).max() - data.low.rolling(window=k).min())
del k

data.dropna(inplace=True)

data['res'] = data['close']
data['res'][:-1] = data['res'][1:]
data = data[:-1]
data['dif'] = np.sign(data.res - data.close)

#%%
data[(data.close < data.sma5)].dif.value_counts()



