# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 10:20:46 2017

@author: aletwhittington
"""

def strat_sim(lngma, shtma, atr_cond, dayspass, symbol):
    
import quandl
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"
#Stocks
chk = quandl.get("WIKI/CHK")

#create moving average
long_ma = 300
short_ma = 60
chk['openlongma'] = pd.rolling_mean(chk['Adj. Open'],long_ma)
chk['openshortma'] = pd.rolling_mean(chk['Adj. Open'],short_ma)

#chk2 = chk.dropna()

    
#Calculate ATR
chk['rownum'] = np.zeros(len(chk))  
Count_Row=chk.shape[0] #gives number of row count
rows_Col=chk.shape[1]-1
for i in range (len(chk)): #create column of row numbers
    chk.iloc[i,rows_Col] = int(i)
    
chk['H-L'] = abs(chk['Adj. High']-chk['Adj. Low'])
chk['H-PDC'] = abs(chk['Adj. High']-chk['Adj. Close'].shift(1))
chk['PDC-L'] = abs(chk['Adj. Close'].shift(1) - chk['Adj. Low'])
chk['TR'] = chk[['H-L','H-PDC','PDC-L']].max(axis=1)
chk['TR ma'] = pd.rolling_mean(chk['TR'],20)
chk.drop(['H-L','H-PDC','PDC-L'], axis=1, inplace=True) #drops columns in original dataframe

chk2 = chk

chk2['ATR'] = np.zeros(len(chk2))
chk2['ATR'] = np.where(chk2['rownum']==19, chk2.iloc[19,16],0)
chk2.loc[chk2['rownum']>19, 'ATR'] = (chk2['TR']/20) + (chk2['ATR'].shift(1)*19/20)

# Identify Buy Threshold by ATR
atr_mult = 1.5
chk2['buy threshold'] = chk2['openlongma'] + (chk2['ATR']*1.5)
chk2['crossover buy'] = 0
# Identify Buy
chk2['buy'] = 0
chk2 = chk2.dropna()
chk2.loc[(chk2['openshortma']>chk2['buy threshold']) & (chk2['openshortma'].shift(1)<=chk2['buy threshold'].shift(1)), 'buy'] = 1

# Identify Sell - using Cross over criteria
#chk2['sell'] = 0
#chk2.loc[(chk2['openshortma']<chk2['openlongma']) & (chk2['openshortma'].shift(1)>=chk2['openlongma'].shift(1)), 'sell'] = 1

 # Identify Sell Strategy - using Days Past the Buy date
chk2['sell'] = 0
chk2.loc[chk2['buy'].shift(50)==1, 'sell'] = 1

# Set Group numbers to each trade
row_buy = chk2['rownum'].where(chk2['buy']==1).dropna().reset_index()
row_buy.columns=['buy date', 'buy row']
row_sell = chk2['rownum'].where(chk2['sell']==1).dropna().reset_index()
row_sell.columns=['sell date', 'sell row']
row_trades = pd.concat([row_buy,row_sell], axis=1)

chk2['trade group'] = 0
for buy in range(len(row_trades)):
    buyrow = row_trades.iloc[buy,1]
    sellrow = row_trades.iloc[buy,3]
    chk2.loc[(chk2['rownum'] >= buyrow) & (chk2['rownum']<=sellrow), 'trade group'] = buyrow
    

# calculate daily returns and cumulate over group ids
chk2['return'] = (chk2['Adj. Open']/chk2['Adj. Open'].shift(1))
chk2.loc[chk2['buy'] == 1, 'return'] = 1 # set start of each group to zero % return
chk2['cumreturn'] = chk2.groupby('trade group')['return'].cumprod()

# Calculate downside standard deviations
chk2['negative returns'] = chk2['return'].map(lambda x: (x-1) if x < 1 else 0)

#summarize Results

return_summary = pd.concat([chk2.groupby('trade group')['cumreturn'].last(), chk2.groupby('trade group')['cumreturn'].count()], axis=1)
return_summary.columns = ['return','days']
return_summary['annulized return'] = (daysell['return']**(251/daysell['days'])) - 1




