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
        return np.log(self.ticker_pull())

    def pct_series(self):
        return self.ticker_pull().pct_change()
        
    def hist_plot(self, trans='level'):
        if trans=='log':
            plt.plot(self.log_series(), label=self.quandlcode)
            plt.xticks(rotation='vertical')
            plt.legend(loc='best') 
        elif trans=='percent':
            plt.hist(self.pct_series().dropna(),bins=20, label=self.quandlcode)
            plt.legend(loc='best')
        else:
            plt.plot(self.ticker_pull(), label=self.quandlcode)
            plt.xticks(rotation='vertical')
            plt.legend(loc='best')           
        
    


tck = Ticker('WIKI/FB', '2015-01-01', 'monthly')

test = tck.ticker_pull()

ploty = tck.hist_plot(1)

pct = tck.pct_series()

            plt.hist(pct.values,bins=20)
            plt.legend(loc='best')