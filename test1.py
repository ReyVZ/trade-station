#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  1 19:49:54 2019

@author: aviz
"""
#%%
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model, model_selection
plt.style.use('seaborn')

#%%
data = pd.read_csv('gkfx_data_1d/EURUSD_1900-04-29_2019-04-29_quotes_1440.csv',
                   parse_dates=[0], header=None, 
                   names=['date', 'open', 'high', 'low', 'close', 'vol'])
data = data[data.vol!=0]

#%%
for _ in [5, 20, 50, 100]:
    col_name = 'sma' + str(_)
    data[col_name] = data.close.rolling(window=_).mean()
    del col_name

#%%
k = 10
data['stoch'] = (data.close - data.low.rolling(window=k).min()) / \
    (data.high.rolling(window=k).max() - data.low.rolling(window=k).min())
del k

#%%
data.dropna(inplace=True)

#%%
days = 1
x = data.iloc[:-days, 1:].values
y = data.close[days:].values

#%%
model = linear_model.LinearRegression()
model_selection.cross_val_score(model, x, y, cv=5).mean()

#%%
model = linear_model.LinearRegression()
model.fit(x[100:], y[100:])

#%%
index = list(range(25))
y_pred = model.predict(x[:100])
fig = plt.figure(figsize=(10, 5))
plt.plot(index, y_pred[:25], index, y[:25])




