# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 12:51:18 2017

@author: aletwhittington
"""

import quandl
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"
#Stocks
fb = quandl.get("WIKI/FB")
goog = quandl.get("WIKI/GOOG")
chk = quandl.get("WIKI/CHK")
vix = quandl.get("CBOE/VIX") #VIX

#functions
def age_yr():
    if 'week' in age:
        a = int(age.split(' ')[0])/52
    elif 'year' in age:
        a = int(age.split(' ')[0])
    return float(a)
train['ageoutcome'] = train['ageoutcome'].fillna('0 years')
train['ageoutcome'] = train['ageoutcome'].map(age_yr)
train['ageoutcome'] = train['ageoutcome'].map(lambda age: age.split(' ')[0])
train['ageoutcome-lag1'] = train['ageoutcome'].shift(1)


chk['close ma'] = pd.rolling_mean(chk['Close'],2)
for i in range(360):
    chk.iloc[]
def atr():
    x = max(opn, cls)
    

quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"
#Stocks
fb = quandl.get("WIKI/FB")
goog = quandl.get("WIKI/GOOG")
chk = quandl.get("WIKI/CHK")
