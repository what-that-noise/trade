# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 14:15:04 2017

@author: aletwhittington
"""

import pandas as pd
import quandl
import matplotlib.pyplot as plt
import math
import timeit
import numpy as np
#import sys
#sys.path.insert(0, "/Users/aletwhittington/Documents/Python_Scripts/Trade")
quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"

class Ticker:
    "base ticker class"
    
    def __init__(self, quandlcode, start, interval):
        self.quandlcode=quandlcode + ".11"
        self.start=start
        self.interval=interval
        
    def ticker_pull(self):
        
        print("DataFrame output of "+ self.quandlcode)
        return quandl.get(self.quandlcode, start_date=self.start, collapse=self.interval)
        
    def log_series(self):
        log = np.log(self.ticker_pull())
        log.columns=[self.quandlcode+"_"+log.columns[0]+'_log']
        return log

    def pct_series(self):
        pct = self.ticker_pull().pct_change()
        pct.columns=[self.quandlcode+"_"+pct.columns[0]+'_return']
        return pct
        
    def hist_plot(self, trans='level'):
        if trans=='log':
            plt.plot(self.log_series(), label=self.quandlcode)
            plt.xticks(rotation='vertical')
            plt.legend(loc='best') 
        elif trans=='percent':
            plt.hist(self.pct_series().dropna().values, bins=15, label=self.quandlcode)
            plt.legend(loc='best')
        else:
            plt.plot(self.ticker_pull(), label=self.quandlcode)
            plt.xticks(rotation='vertical')
            plt.legend(loc='best')           
        
    
class Portfolio_Character:
    
    "note: enter tickers as a string '[fb_tck, amzn_tck, xom_tck]'"
    
    def __init__(self, weights, tickers):
        self.weights = weights
        self.tickers = tickers
        if len(self.weights) != len(self.tickers):
            print("# of weights must equal # of assets/stocks/tickersymbols")
        
        #print("Weights: ", self.weights, "Tickers = ", self.tickers.tolist())
    
    def create_portfolio(self):
        prt = pd.concat(eval(self.tickers), axis=1).dropna()
        prt.columns=[self.tickers.strip('[]').split(',')]
        return prt

    def weighted_return_series(self):
              
        print(pd.Series(self.weights, index=self.create_portfolio().columns))
        return pd.DataFrame(100*(self.create_portfolio().dot(pd.Series(self.weights, index=self.create_portfolio().columns))))

    def weighted_return(self):
        
        return self.weighted_return_series().mean()
                
    def weighted_annual_return(self):
        
        return self.weighted_return_series().mean()*12
        
    def plot_returns(self):
        plt.hist(self.weighted_return_series.dropna(),bins=15, label="portfolio_Return")
        plt.legend(loc='best')
        
    def portfolio_std(self):
        
        return math.sqrt(pd.Series(self.weights, index=self.create_portfolio().columns).transpose().values @ self.create_portfolio().cov(min_periods=1).values @ pd.Series(self.weights, index=self.create_portfolio().columns).values)
        
    def sharpe_ratio(self):
        
        return self.weighted_return()/self.portfolio_std()
        
    def portfolio_summary(self):
        
        w_df = pd.DataFrame([self.weights])
        w_df.columns=[self.create_portfolio().columns]
        sr_df = pd.DataFrame(self.sharpe_ratio())
        sr_df.columns=['Sharpe_Ratio']
        war_df = pd.DataFrame(self.weighted_annual_return())
        war_df.columns=['Portfolio_Annual_Return']
        std_df = pd.DataFrame([self.portfolio_std()])
        std_df.columns=['Portfolio_Stdev']
        
        return pd.concat([sr_df, war_df, std_df, w_df], axis=1)


###    TEST

fb = Ticker('WIKI/FB', '2015-01-01', 'monthly')
amzn = Ticker('WIKI/AMZN', '2015-01-01', 'monthly')
xom = Ticker('WIKI/XOM', '2015-01-01', 'monthly')

fb_tck = fb.pct_series()
fb_tck = fb.ticker_pull()
amzn_tck = amzn.pct_series()
xom_tck = xom.pct_series()

p = Portfolio_Character([.25,.25,.50], '[fb_tck, amzn_tck, xom_tck]')
port = p.create_portfolio()
p.weighted_annual_return()

            plt.hist(fb_tck.dropna().values, label='fb')
            plt.legend(loc='best')
### END

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

tck = Ticker('WIKI/FB', '2015-01-01', 'monthly')

lgs = tck.log_series()
test = tck.ticker_pull()

ploty = tck.hist_plot(1)

pct = tck.pct_series()
testy2 = pd.concat([pct,pct], axis=1).dropna()
plt.hist(pct.values,bins=20)
plt.legend(loc='best')