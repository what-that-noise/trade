# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:28:29 2017

@author: aletwhittington
"""

import quandl
quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"
import matplotlib.pyplot as plt
import pandas as pd
quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"
import matplotlib.pyplot as plt
import math

#data = quandl.get("WIKI/FB.11", start_date="2014-01-01", end_date="2014-12-31", collapse="monthly", transform="diff")
# All Historical Data
"""
amzn = quandl.get("WIKI/AMZN") #amazon
xom = quandl.get("WIKI/XOM") #Exxon mobil
aapl = quandl.get("WIKI/AAPL") # apple
cof = quandl.get("WIKI/COF") #capone
"""
# Select Time Range and snapshot frequency
start = "1990-01-01" #cannot be empty
snapshot = "monthly" #leave empty "" for daily default
amzn = quandl.get("WIKI/AMZN.11", start_date=start, collapse=snapshot)
xom = quandl.get("WIKI/XOM.11", start_date=start, collapse=snapshot)
aapl = quandl.get("WIKI/AAPL.11", start_date=start, collapse=snapshot)
cof = quandl.get("WIKI/COF.11", start_date=start, collapse=snapshot)


amzn['Log Price'] = np.log(amzn['Adj. Close'])
xom['Log Price'] = np.log(xom['Adj. Close'])
aapl['Log Price'] = np.log(aapl['Adj. Close'])
cof['Log Price'] = np.log(cof['Adj. Close'])

amzn['return pct'] = 100*(amzn['Adj. Close'].pct_change())
xom['return pct'] = 100*(xom['Adj. Close'].pct_change())
aapl['return pct'] = 100*(aapl['Adj. Close'].pct_change())
cof['return pct'] = 100*(cof['Adj. Close'].pct_change())


portfolio = pd.concat([amzn['return pct'], xom['return pct'], aapl['return pct'], cof['return pct']], axis=1).dropna() 
portfolio.columns=['amzn_return_pct', 'xom_return_pct', 'aapl_return_pct', 'cof_return_pct']
portfolio.corr(method='pearson', min_periods=1)

#Assign Weights
w = [.25,.25,.25,.25]

weights = pd.Series(w, index=portfolio.columns)

portfolio['weighted_return_pct']=portfolio.dot(weights)

#Calculated Weighted Average Portfolio Return
port_return = portfolio['weighted_return_pct'].mean()

#Calculated Weighted Average Portfolio Variance
  #var = w1^2*var1 + w2^2*var2 + 2*w1*w2*cov1,2
cov_matrix = portfolio.drop('weighted_return_pct', axis=1).cov(min_periods=1)
asset_var = portfolio.drop('weighted_return_pct', axis=1).var(axis=0)
w2 = weights**2
var_comp = (asset_var*w2).sum()

#Graph Comparisons in Log Scale
port_log = pd.concat([amzn['Log Price'], xom['Log Price'], aapl['Log Price'], cof['Log Price']], axis=1) 
port_log.columns=['amzn_log', 'xom_log', 'aapl_log', 'cof_log']

plt.plot(port_log['amzn_log'], label='amzn')
plt.plot(port_log['xom_log'], label='xom')
plt.plot(port_log['aapl_log'], label='aapl') 
plt.plot(port_log['cof_log'], label='cof') 
plt.xticks(rotation='vertical')
plt.legend(loc='best') 

############################# Under Consideration 

do = quandl.get("WIKI/DO") #Diamond Offshore Drilling, Inc.

wmt = quandl.get("WIKI/WMT") #walmart
cost = quandl.get("WIKI/COST") # Costco

msft = quandl.get("WIKI/MSFT") #Microsoft

wfc = quandl.get("WIKI/WFC") #Wellsfargo
bbt = quandl.get("WIKI/BBT") # bbt
trv = quandl.get("WIKI/TRV") # travelers

