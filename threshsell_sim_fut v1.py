# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 17:58:21 2017

@author: aletwhittington
"""

quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"
q = quandl.get("WIKI/CHK")
import quandl
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm

def strat_sim(lngma, shtma, atr_cond, dayspass):
    print(lngma, shtma, atr_cond, dayspass)
    #lngma, shtma, atr_cond, dayspass = 60, 5, 0, 20
    
    tck = q.copy()#quandl.get("WIKI/CHK")
    
    #create moving average based on parameters
    long_ma = lngma
    short_ma = shtma
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
    atr_mult = atr_cond
    tck2['buy threshold'] = tck2['openlongma'] + (tck2['ATR']*atr_mult)
    
    # Trigger Buy
    tck2['buy'] = 0
    tck2 = tck2.dropna()
    tck2.loc[(tck2['openshortma']>tck2['buy threshold']) & (tck2['openshortma'].shift(1)<=tck2['buy threshold'].shift(1)), 'buy'] = 1
    
    # Identify Sell - using Cross over criteria
    #tck2['sell'] = 0
    #tck2.loc[(tck2['openshortma']<tck2['openlongma']) & (tck2['openshortma'].shift(1)>=tck2['openlongma'].shift(1)), 'sell'] = 1
    
     # Identify Sell Strategy - using Days Past the Buy date
    tck2['sell'] = 0
    tck2.loc[tck2['buy'].shift(dayspass)==1, 'sell'] = 1

    
    # Set Group numbers to each trade
    row_buy = tck2['rownum'].where(tck2['buy']==1).dropna().reset_index()
    row_buy.columns=['buy date', 'buy row']
    row_sell = tck2['rownum'].where(tck2['sell']==1).dropna().reset_index()
    row_sell.columns=['sell date', 'sell row']
    row_trades = pd.concat([row_buy,row_sell], axis=1).dropna()
    
    tck2['trade group'] = 0
    for buy in range(len(row_trades)):
        buyrow = row_trades.iloc[buy,1]
        sellrow = row_trades.iloc[buy,3]
        tck2.loc[(tck2['rownum'] >= buyrow) & (tck2['rownum']<=sellrow), 'trade group'] = buyrow
        
    
    # calculate daily returns and cumulate over trade group ids
    tck2['return'] = (tck2['Adj. Open']/tck2['Adj. Open'].shift(1)).fillna(1)
    tck2.loc[tck2['buy'] == 1, 'return'] = 1 # set start of each group to zero % return
    tck2['cumreturn'] = tck2.groupby('trade group')['return'].cumprod()
    
    
    # Calculate cummulative return over strategy
    tck2['returns on trades'] = 1
    tck2.loc[tck2['trade group'] > 0 , 'returns on trades'] = tck2['return']
    tck2['cumreturn strategy'] = tck2['returns on trades'].cumprod()
    
    
    # Calculate Max Drawdowns from Trades
    tck2['cumreturn trade'] = tck2['returns on trades'].groupby(tck2['trade group']).cumprod()
    row_trades['diff'] = row_trades['sell row'] - row_trades['buy row']
    tck2['drawdown'] = 0
    for i in range(len(row_trades)):
        grp_id = int(row_trades.iloc[i,1])
        days = int(row_trades.iloc[i,4])
        tck2.loc[tck2['trade group'] == grp_id, 'drawdown'] = (tck2['cumreturn trade'] - tck2['cumreturn trade'].rolling(days).max().shift(1)).fillna(0)
    
    tck2.drop(['cumreturn trade'], axis=1, inplace=True)
    
    # Calculate downside standard deviations
    tck2['negative returns sqrd'] = tck2['return'].map(lambda x: (x-1)**2 if x < 1 else 0)
    
    
    #summarize Results at Trade Level
    
    ## Equity Curve
    ##investment = 1000
    ##equity_curve = tck2['cumreturn strategy'] * investment
    ##plt.plot(tck2['cumreturn strategy'])
    
    return_summary = pd.concat([tck2.groupby('trade group')['cumreturn'].last()-1,(tck2.groupby('trade group')['cumreturn'].last()**(251/tck2.groupby('trade group')['cumreturn'].count()))-1, tck2.groupby('trade group')['cumreturn'].count(), tck2.groupby('trade group')['negative returns sqrd'].sum()/tck2.groupby('trade group')['negative returns sqrd'].count()**0.5, ((251/tck2.groupby('trade group')['negative returns sqrd'].count())**0.5)*((tck2.groupby('trade group')['negative returns sqrd'].sum()/tck2.groupby('trade group')['negative returns sqrd'].count())**0.5), tck2.groupby('trade group')['drawdown'].max()], axis=1)
    return_summary.columns = ['rate of return on trade','rate of return for trade annlzd','days of trade', 'downside dev','downside dev annlzd', 'max drawdown']
    return_summary = return_summary.reset_index()
    return_trades = return_summary.where(return_summary['trade group']>0).dropna()
    return_trades_avg = (return_trades['rate of return for trade annlzd'].mean())
    num_trades = (return_trades['rate of return for trade annlzd'].count())
    #return_summary['Sortino Ratio Anualzd'] = return_summary['rate of return for trade annlzd']/return_summary['downside dev annlzd']
    
    #return_summary_filtered = return_summary.where((return_summary['trade group']>0) & (return_summary['days of trade']>49) & (return_summary['rate of return for trade annlzd']<10)).dropna()
   # plt.hist(return_summary['rate of return for trade annlzd'].where(return_summary['rate of return for trade annlzd']<10).dropna(), bins=len(return_summary['rate of return for trade annlzd'].where(return_summary['rate of return for trade annlzd']<10).dropna()))
    # MAR = Average returns from Trades / Max Drawdown across all trades
    # R ratio = Sum of positive returns divided by sum of negative returns
    
    #summarize Results at Strategy Level
    tck2['cumreturn buyhold'] = tck2['return'].cumprod()
    tck3 = tck2.reset_index()
    ###days_of_strategy = (tck3['Date'].max() - tck3['Date'].min()).days
    start = tck3['Date'].min()
    end = tck3['Date'].max()
    converter_to_annual = 365/((tck3['Date'].max() - tck3['Date'].min()).days)
    years = ((tck3['Date'].max() - tck3['Date'].min()).days)/365
    trades_per_yr = num_trades/years
    mean_annl_rtn_pct_strat = float(100*((tck3['cumreturn strategy'].tail(1)**converter_to_annual)-1))
    mean_annl_rtn_pct_buyhold = float(100*((tck3['cumreturn buyhold'].tail(1)**converter_to_annual)-1))       
    ## MAR = Average returns from Trades / Max Drawdown across all trades
    max_drawdown = abs(tck3['drawdown'].min())
    mar = float((mean_annl_rtn_pct_strat/100) / max_drawdown)
    ## Sortino
    dwnsd = tck3.where(tck3['trade group']>0).dropna()
    downside_dev = (dwnsd['negative returns sqrd'].sum()/dwnsd['negative returns sqrd'].count())**0.5
    downside_dev_annl = (365**0.5)*downside_dev
    sortino = float((mean_annl_rtn_pct_strat/100)/downside_dev_annl)
    ## Sharp
    std_dev_annl = (365**0.5)*dwnsd['return'].std()
    sharp = float((mean_annl_rtn_pct_strat/100)/std_dev_annl)
    
    #FINAL OUTPUT
    strat_summary = pd.DataFrame([start, end, years, trades_per_yr, mean_annl_rtn_pct_strat, mean_annl_rtn_pct_buyhold, mean_annl_rtn_pct_strat - mean_annl_rtn_pct_buyhold, return_trades_avg, 100*max_drawdown, mar, sortino, sharp, lngma, shtma, atr_cond, dayspass]).T
    strat_summary.columns=['start','end', 'years', 'tradesperyear', 'mean_annl_pct_return_strat', 'mean_annl_pct_return_buyhold', 'annual_return_strat_over_buyhold', 'mean_annl_pct_return_trd_avg', 'max_drawdown_pct', 'mar', 'Sortino_Ratio_annl', 'Sharp_Ratio_annl', 'long_ma', 'short_ma', 'atr_thrshld', 'days_in_trade']
   
    return strat_summary
# Test output = strat_sim(50, 10, 0.5, 25)
"""
gbl = globals()
for i in range(300,320,10): 
    #gbl['output_'+str(i)] = strat_sim(i, 60, 1.5, 50)
    output = pd.concat([output,strat_sim(i, 60, 1.5, 50)])
output.to_csv('/Users/aletwhittington/Documents/Python_Scripts/trade/searchresults.csv',header=True)
#######
    """

#Run Search
q = quandl.get("WIKI/MSFT")
######Initialize table
output = pd.DataFrame([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).T
output.columns=['start','end', 'years', 'tradesperyear', 'mean_annl_pct_return_strat', 'mean_annl_pct_return_buyhold', 'annual_return_strat_over_buyhold', 'mean_annl_pct_return_trd_avg', 'max_drawdown_pct', 'mar', 'Sortino_Ratio_annl', 'Sharp_Ratio_annl', 'long_ma', 'short_ma', 'atr_thrshld', 'days_in_trade']
for i in range(50,80,10): # longma #5 1:45min expected run time
    for j in range (5, 25, 5): #shortma 5
        for k in range(0, 20, 5): #ATR 5
            k2 = k/10
            for l in range(10, 40, 10): #days in trade 4
#Collect results
                output = pd.concat([output,strat_sim(i, j, k2, l)])
                #gbl['output_'+str(i)+str(j)+str(k)+str(l)] = strat_sim(i, j, k, l)                
                #gbl['output_'+str(i)+str(j)+str(k)+str(l)] = strat_sim(300, 60, 1.5, 50)
output['tck'] ='MSFT'
output.to_csv('/Users/aletwhittington/Documents/Python_Scripts/trade/searchresults_MSFT.csv',header=True)

q = quandl.get("WIKI/INTC")
output = pd.DataFrame([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).T
output.columns=['start','end', 'years', 'tradesperyear', 'mean_annl_pct_return_strat', 'mean_annl_pct_return_buyhold', 'annual_return_strat_over_buyhold', 'mean_annl_pct_return_trd_avg', 'max_drawdown_pct', 'mar', 'Sortino_Ratio_annl', 'Sharp_Ratio_annl', 'long_ma', 'short_ma', 'atr_thrshld', 'days_in_trade']
for i in range(50,80,10): # longma #5 1:45min expected run time
    for j in range (5, 25, 5): #shortma 5
        for k in range(0, 20, 5): #ATR 5
            k2 = k/10
            for l in range(10, 40, 10): #days in trade 4
#Collect results
                output = pd.concat([output,strat_sim(i, j, k2, l)])
                #gbl['output_'+str(i)+str(j)+str(k)+str(l)] = strat_sim(i, j, k, l)                
                #gbl['output_'+str(i)+str(j)+str(k)+str(l)] = strat_sim(300, 60, 1.5, 50)
output['tck'] ='INTC'
output.to_csv('/Users/aletwhittington/Documents/Python_Scripts/trade/searchresults_INTC.csv',header=True)

q = quandl.get("WIKI/ORCL")
output = pd.DataFrame([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).T
output.columns=['start','end', 'years', 'tradesperyear', 'mean_annl_pct_return_strat', 'mean_annl_pct_return_buyhold', 'annual_return_strat_over_buyhold', 'mean_annl_pct_return_trd_avg', 'max_drawdown_pct', 'mar', 'Sortino_Ratio_annl', 'Sharp_Ratio_annl', 'long_ma', 'short_ma', 'atr_thrshld', 'days_in_trade']
for i in range(50,80,10): # longma #5 1:45min expected run time
    for j in range (5, 25, 5): #shortma 5
        for k in range(0, 20, 5): #ATR 5
            k2 = k/10
            for l in range(10, 40, 10): #days in trade 4
#Collect results
                output = pd.concat([output,strat_sim(i, j, k2, l)])
                #gbl['output_'+str(i)+str(j)+str(k)+str(l)] = strat_sim(i, j, k, l)                
                #gbl['output_'+str(i)+str(j)+str(k)+str(l)] = strat_sim(300, 60, 1.5, 50)
output['tck'] ='ORCL'
output.to_csv('/Users/aletwhittington/Documents/Python_Scripts/trade/searchresults_ORCL.csv',header=True)




######################################
#           Regression on Parameters
######################################
#return over buyhold
results_ols = smf.ols(formula='y~x +x', data=ch).fit()
print(results_ols.summary())

#sortino
output2 = output.reset_index()
y_sort = output2['Sortino Ratio annl']
X = pd.DataFrame(output2['long ma']).join(output2['short ma']).join(output2['atr thrshld']).join(output2['days in trade'])
results_ols = sm.OLS(y_sort.astype(float),X.astype(float)).fit() 
print(results_ols.summary())
