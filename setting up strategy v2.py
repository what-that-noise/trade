# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 12:51:18 2017

@author: aletwhittington
"""

import quandl
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import numpy as np

quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"
#Stocks
#fb = quandl.get("WIKI/FB")
#goog = quandl.get("WIKI/GOOG")
chk = quandl.get("WIKI/CHK")
#vix = quandl.get("CBOE/VIX") #VIX

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
for i in range (len(chk)):
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
chk2['crossover buy'] = 0
chk2 = chk2.dropna()
chk2.loc[(chk2['openshortma']>chk2['buy threshold']) & (chk2['openshortma'].shift(1)<=chk2['buy threshold'].shift(1)), 'crossover buy'] = 1
 # Identify Sell using Cross over criteria
chk2['crossover sell'] = 0
chk2.loc[(chk2['openshortma']<chk2['openlongma']) & (chk2['openshortma'].shift(1)>=chk2['openlongma'].shift(1)), 'crossover sell'] = 1

 # Identify Sell using Days Past Buy date
chk2['days past sell'] = 0
chk2.loc[chk2['crossover buy'].shift(50)==1, 'days past sell'] = 1

#calculate returns
chk2['intrade ind cr sell'] = 0
ind_Col=chk2.shape[1]-1
buy_Col=chk2.shape[1]-4
sell_Col=chk2.shape[1]-3
for i in range(1, len(chk2)):
    j=i-1
    chk2.iloc[i,ind_Col] = abs(chk2.iloc[i,buy_Col]+chk2.iloc[i,sell_Col]-chk2.iloc[j,ind_Col])

chk2['intrade ind days'] = 0
ind_Col=chk2.shape[1]-1
buy_Col=chk2.shape[1]-5
sell_Col=chk2.shape[1]-3
for i in range(1, len(chk2)):
    j=i-1
    chk2.iloc[i,ind_Col] = abs(chk2.iloc[i,buy_Col]+chk2.iloc[i,sell_Col]-chk2.iloc[j,ind_Col])

chk2['group xsell ref'] = 0
chk2.loc[(chk2['intrade ind cr sell']==1) & (chk2['intrade ind cr sell'].shift(1)==0), 'group xsell ref'] = chk2['rownum']


chk2['group xsell'] = 0
grp_xsellCol=chk2.shape[1]-1
ref_Col=chk2.shape[1]-2
ind_Col=chk2.shape[1]-4
for i in range(1, len(chk2)):
    j=i-1
    chk2.iloc[i,grp_xsellCol] = (chk2.iloc[j,grp_xsellCol]+chk2.iloc[i,ref_Col])*chk2.iloc[i,ind_Col]

chk2['group daysell'] = 0
grp_daysellCol=chk2.shape[1]-1
ref_Col=chk2.shape[1]-3
ind_Col=chk2.shape[1]-4
for i in range(1, len(chk2)):
    j=i-1
    chk2.iloc[i,grp_daysellCol] = (chk2.iloc[j,grp_daysellCol]+chk2.iloc[i,ref_Col])*chk2.iloc[i,ind_Col]

chk2['return'] = (chk2['Adj. Open']/chk2['Adj. Open'].shift(1))
chk2.loc[chk2['crossover buy'] == 1, 'return'] = 1
chk2['cumreturn xsell'] = chk2.groupby('group xsell')['return'].cumprod()
chk2['cumreturn daysell'] = chk2.groupby('group daysell')['return'].cumprod()
#chk2['sum'] = chk2.groupby('intrade ind days')['rownum'].cumsum()



#chk2['return cr sell'] = chk2['return']
#chk2.loc[(chk2['intrade ind cr sell'] == 1) & (chk2['intrade ind cr sell'].shift(1)==0),'return cr sell'] = 1


# Initial Investment
investment = 100

# Calculate Average Return on strategy
chk2['investment'] = 0
chk2.loc[chk2['crossover buy']==1, 'investment'] = investment
chk2['investment return']








    
