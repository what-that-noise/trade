# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 13:28:29 2017

@author: aletwhittington
"""

import quandl
quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"
import pandas as pd
import matplotlib.pyplot as plt
import math
import timeit

#data = quandl.get("WIKI/FB.11", start_date="2014-01-01", end_date="2014-12-31", collapse="monthly", transform="diff")
# All Historical Data
"""
amzn = quandl.get("WIKI/AMZN") #amazon
xom = quandl.get("WIKI/XOM") #Exxon mobil
aapl = quandl.get("WIKI/AAPL") # apple
cof = quandl.get("WIKI/COF") #capone
"""
# Select Time Range and snapshot frequency
start = "2009-01-01" #cannot be empty
snapshot = "monthly" #leave empty "" for daily default
amzn = quandl.get("WIKI/AMZN.11", start_date=start, collapse=snapshot)
xom = quandl.get("WIKI/XOM.11", start_date=start, collapse=snapshot)
aapl = quandl.get("WIKI/AAPL.11", start_date=start, collapse=snapshot)
cof = quandl.get("WIKI/COF.11", start_date=start, collapse=snapshot)
fb = quandl.get("WIKI/FB.11", start_date=start, collapse=snapshot)

amzn['Log Price'] = np.log(amzn['Adj. Close'])
xom['Log Price'] = np.log(xom['Adj. Close'])
aapl['Log Price'] = np.log(aapl['Adj. Close'])
cof['Log Price'] = np.log(cof['Adj. Close'])

amzn['return pct'] = 100*(amzn['Adj. Close'].pct_change())
xom['return pct'] = 100*(xom['Adj. Close'].pct_change())
aapl['return pct'] = 100*(aapl['Adj. Close'].pct_change())
cof['return pct'] = 100*(cof['Adj. Close'].pct_change())
fb['return pct'] = 100*(fb['Adj. Close'].pct_change())

portfolio2 = pd.concat([amzn['return pct'], xom['return pct'], aapl['return pct'], cof['return pct']], axis=1).dropna() 
portfolio2.columns=['amzn_return_pct', 'xom_return_pct', 'aapl_return_pct', 'cof_return_pct']
portfolio2.corr(method='pearson', min_periods=1)

#Calculate Metrics

def port_weights(weight_vector):
    print(weight_vector)
    start = timeit.default_timer()
    #w = [.25,.25,.25,.25]
    w = weight_vector
    weights = pd.Series(w, index=portfolio2.columns)
    portfolio = portfolio2.copy()
    portfolio['weighted_return_pct']=portfolio.dot(weights)
    
    #Calculated Weighted Average Portfolio Return
    port_return = portfolio['weighted_return_pct'].mean()
    return_annualized = pd.DataFrame([port_return*12])
    return_annualized.columns=['return_annualized']
    #Calculated Weighted Average Portfolio Variance
            #var = w1^2*var1 + w2^2*var2 + 2*w1*w2*cov1,2
    cov_matrix = portfolio.drop('weighted_return_pct', axis=1).cov(min_periods=1)
           #port_var = weights.transpose().values @ cov_matrix.values @ weights.values
    port_std = math.sqrt(weights.transpose().values @ cov_matrix.values @ weights.values)
    port_std_df = pd.DataFrame([port_std])
    port_std_df.columns=['std']
    #Calculate Sharpe Ratio
    sharpe_ratio = pd.DataFrame([port_return/port_std])
    sharpe_ratio.columns=['sharpe_ratio']
    
    #Summarize
    weight_list = pd.DataFrame([weights.tolist()])
    weight_list.columns=[portfolio2.columns]
    port_summary = pd.concat([sharpe_ratio, return_annualized, port_std_df, weight_list], axis=1)
    stop = timeit.default_timer()
    print((stop - start))
    return port_summary

#Create Simulations
output = pd.DataFrame([]).T
#output.columns=['sharpe_ratio', 'return_annualized', '0','1','2','3']
for i in range(10, 65, 5): 
    i2 = i/100
    for j in range (10, 65, 5): 
        j2 = j/100
        for k in range(5, 35, 5): 
            k2 = k/100
            for l in range(5, 35, 5): 
                l2 = l/100
                weight_vector = [i2,j2,k2,l2]
                
#Collect results
                output = pd.concat([output,port_weights(weight_vector)])
#output['tck'] ='MSFT'
output.to_csv('/Users/aletwhittington/Documents/Python_Scripts/trade/portfolio_weights_2012.csv',header=True)

   """
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

    """
    w = [.45,.1,.30,.15]
    weights = pd.Series(w, index=portfolio2.columns)
    portfolio = portfolio2.copy()
    portfolio['weighted_return_pct']=portfolio.dot(weights)

fb_add = pd.concat([portfolio['weighted_return_pct'],fb['return pct']],axis=1).dropna()
fb_add.corr(method='pearson', min_periods=1)
fb_add.cov(min_periods=1)
fb_add['return pct'].mean()*12
fb_add['weighted_return_pct'].mean()*12
