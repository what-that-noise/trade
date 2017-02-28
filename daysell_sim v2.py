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
tck = quandl.get("WIKI/CHK")

#create moving average
long_ma = 300
short_ma = 60
tck['openlongma'] = pd.rolling_mean(tck['Adj. Open'],long_ma)
tck['openshortma'] = pd.rolling_mean(tck['Adj. Open'],short_ma)

#tck2 = tck.dropna()

    
#Calculate ATR
tck['rownum'] = np.zeros(len(tck))  
Count_Row=tck.shape[0] #gives number of row count
rows_Col=tck.shape[1]-1
for i in range (len(tck)): #create column of row numbers
    tck.iloc[i,rows_Col] = int(i)
    
tck['H-L'] = abs(tck['Adj. High']-tck['Adj. Low'])
tck['H-PDC'] = abs(tck['Adj. High']-tck['Adj. Close'].shift(1))
tck['PDC-L'] = abs(tck['Adj. Close'].shift(1) - tck['Adj. Low'])
tck['TR'] = tck[['H-L','H-PDC','PDC-L']].max(axis=1)
tck['TR ma'] = pd.rolling_mean(tck['TR'],20)
tck.drop(['H-L','H-PDC','PDC-L'], axis=1, inplace=True) #drops columns in original dataframe

tck2 = tck

tck2['ATR'] = np.zeros(len(tck2))
tck2['ATR'] = np.where(tck2['rownum']==19, tck2.iloc[19,16],0)
tck2.loc[tck2['rownum']>19, 'ATR'] = (tck2['TR']/20) + (tck2['ATR'].shift(1)*19/20)

# Identify Buy Threshold by ATR
atr_mult = 1.5
tck2['buy threshold'] = tck2['openlongma'] + (tck2['ATR']*1.5)
tck2['crossover buy'] = 0
# Identify Buy
tck2['buy'] = 0
tck2 = tck2.dropna()
tck2.loc[(tck2['openshortma']>tck2['buy threshold']) & (tck2['openshortma'].shift(1)<=tck2['buy threshold'].shift(1)), 'buy'] = 1

# Identify Sell - using Cross over criteria
#tck2['sell'] = 0
#tck2.loc[(tck2['openshortma']<tck2['openlongma']) & (tck2['openshortma'].shift(1)>=tck2['openlongma'].shift(1)), 'sell'] = 1

 # Identify Sell Strategy - using Days Past the Buy date
tck2['sell'] = 0
tck2.loc[tck2['buy'].shift(50)==1, 'sell'] = 1

# Set Group numbers to each trade
row_buy = tck2['rownum'].where(tck2['buy']==1).dropna().reset_index()
row_buy.columns=['buy date', 'buy row']
row_sell = tck2['rownum'].where(tck2['sell']==1).dropna().reset_index()
row_sell.columns=['sell date', 'sell row']
row_trades = pd.concat([row_buy,row_sell], axis=1)

tck2['trade group'] = 0
for buy in range(len(row_trades)):
    buyrow = row_trades.iloc[buy,1]
    sellrow = row_trades.iloc[buy,3]
    tck2.loc[(tck2['rownum'] >= buyrow) & (tck2['rownum']<=sellrow), 'trade group'] = buyrow
    

# calculate daily returns and cumulate over group ids
tck2['return'] = (tck2['Adj. Open']/tck2['Adj. Open'].shift(1)).fillna(1)
tck2.loc[tck2['buy'] == 1, 'return'] = 1 # set start of each group to zero % return
tck2['cumreturn'] = tck2.groupby('trade group')['return'].cumprod()

# Calculate downside standard deviations
tck2['negative returns'] = tck2['return'].map(lambda x: (x-1)**2 if x < 1 else 0)


# Calculate strategy returns over time
tck2['returns on trades'] = 1
tck2.loc[tck2['trade group'] > 0 , 'returns on trades'] = tck2['return']
tck2['cumreturn trades'] = tck2['returns on trades'].cumprod()

#summarize Results
investment = 1000
tck2['equity curve'] = tck2['cumreturn trades'] * investment
return_summary = pd.concat([tck2.groupby('trade group')['cumreturn'].last(), tck2.groupby('trade group')['cumreturn'].count(), ((251/tck2.groupby('trade group')['negative returns'].count())**0.5)*((tck2.groupby('trade group')['negative returns'].sum()/tck2.groupby('trade group')['negative returns'].count())**0.5)], axis=1)
return_summary.columns = ['return','days', 'downside dev annulzd']
return_summary = return_summary.reset_index()
return_summary['annualized return'] = (return_summary['return']**(251/return_summary['days'])) - 1
return_summary['Sortino Ratio Anualzd'] = return_summary['annualized return']/return_summary['downside dev annulzd']
return_summary_filtered = return_summary.where((return_summary['trade group']>0) & (return_summary['days']>49) & (return_summary['annualized return']<10)).dropna()
plt.hist(return_summary['annualized return'].where(return_summary['annualized return']<10).dropna(), bins=len(return_summary['annualized return'].where(return_summary['annualized return']<10).dropna()))
plt.plot(tck2['equity curve'])
#((251/tck2.groupby('trade group')['negative returns'].count())**0.5)*((tck2.groupby('trade group')['negative returns'].sum()/tck2.groupby('trade group')['negative returns'].count())**0.5)