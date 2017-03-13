# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 11:51:44 2017

@author: aletwhittington
"""

#Steps 
## 1) Find companies within industries
## 2) Find companies within industries that have high correlations and low correlations
##    with other companies in industry and outside industry
## 3) Develop strategies and test on high correlated companies
## 4) Choose companies from industries that are leading indicators for trend strategies
## 5) 

import quandl
import matplotlib.pyplot as plt
import pandas as pd
quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"
import matplotlib.pyplot as plt
import math

#results_ols = smf.ols(formula='y~x +x', data=ch).fit()
#print(results_ols.summary())

#ENERGY
chk = quandl.get("WIKI/CHK") #Chesapeake
rig = quandl.get("WIKI/RIG") #Transocean Limted
do = quandl.get("WIKI/DO") #Diamond Offshore Drilling, Inc.
xom = quandl.get("WIKI/XOM") #Exxon mobil
chk['return pct'] = 100*(chk['Adj. Close'].pct_change())
chk['returnma'] = pd.rolling_mean(chk['return pct'],30)
rig['return pct'] = 100*(rig['Adj. Close'].pct_change())
rig['returnma'] = pd.rolling_mean(rig['return pct'],30)
do['return pct'] = 100*(do['Adj. Close'].pct_change())
do['returnma'] = pd.rolling_mean(do['return pct'],30)
xom['return pct'] = 100*(xom['Adj. Close'].pct_change())
xom['returnma'] = pd.rolling_mean(xom['return pct'],30)
energy = pd.concat([chk['returnma'], rig['returnma'], do['returnma'], xom['returnma']], axis=1) 
energy.columns=['chk', 'rig', 'do', 'xom']
energy.corr(method='pearson', min_periods=1)

chk['Log Price'] = np.log(chk['Adj. Close'])
rig['Log Price'] = np.log(rig['Adj. Close'])
do['Log Price'] = np.log(do['Adj. Close'])
xom['Log Price'] = np.log(xom['Adj. Close'])

# plt.plot(chk['Log Price'], label='chk')# volatility is sign. higher than others. Same strategy would be ineffective
plt.plot(rig['Log Price'], label='rig')
plt.plot(do['Log Price'], label='do')
#plt.plot(xom['Log Price'], label='xom') #much less volatile due to company diversification and same strategy unlikely to work
plt.xticks(rotation='vertical')
plt.legend(loc='best') 

#Oil gas midstream
psx = quandl.get("WIKI/PSX") #Phillups 66
mpc = quandl.get("WIKI/MPC") #Marathon Petroleum Corporation
psx['return pct'] = 100*(psx['Adj. Close'].pct_change())
psx['returnma'] = pd.rolling_mean(psx['return pct'],30)
mpc['return pct'] = 100*(mpc['Adj. Close'].pct_change())
mpc['returnma'] = pd.rolling_mean(mpc['return pct'],30)
midstream = pd.concat([psx['returnma'], mpc['returnma']], axis=1) 
midstream.columns=['psx', 'mpc']
midstream.corr(method='pearson', min_periods=1)

psx['Log Price'] = np.log(psx['Adj. Close'])
mpc['Log Price'] = np.log(mpc['Adj. Close'])

plt.plot(psx['Log Price'], label='psx') # less volatility than Marathon Petrol same strategy should be effective with less drawdown
plt.plot(mpc['Log Price'], label='mpc')
plt.xticks(rotation='vertical')
plt.legend(loc='best') 

#AIRLINES
aal = quandl.get("WIKI/AAL") #American
luv = quandl.get("WIKI/LUV") #Southwest
dal = quandl.get("WIKI/DAL") # Delta Airlines
alk = quandl.get("WIKI/ALK") #Air Alaska
aal['return pct'] = 100*(aal['Adj. Close'].pct_change())
aal['returnma'] = pd.rolling_mean(aal['return pct'],30)
luv['return pct'] = 100*(luv['Adj. Close'].pct_change())
luv['returnma'] = pd.rolling_mean(luv['return pct'],30)
dal['return pct'] = 100*(dal['Adj. Close'].pct_change())
dal['returnma'] = pd.rolling_mean(dal['return pct'],30)
alk['return pct'] = 100*(alk['Adj. Close'].pct_change())
alk['returnma'] = pd.rolling_mean(alk['return pct'],30)
airlines = pd.concat([aal['returnma'], luv['returnma'], dal['returnma'], alk['returnma']], axis=1) 
airlines.columns=['aal', 'luv', 'dal', 'alk']
airlines.corr(method='pearson', min_periods=1)

aal['Log Price'] = np.log(aal['Adj. Close'])
luv['Log Price'] = np.log(luv['Adj. Close'])
dal['Log Price'] = np.log(dal['Adj. Close'])
alk['Log Price'] = np.log(alk['Adj. Close'])

plt.plot(aal['Log Price'], label='aal') #highest volatility meaning larger drawdowns - strat should still work
plt.plot(luv['Log Price'], label='luv')
plt.plot(dal['Log Price'], label='dal')
plt.plot(alk['Log Price'], label='alk')
plt.xticks(rotation='vertical')
plt.legend(loc='best') 

#MARKETING
fb = quandl.get("WIKI/FB")
goog= quandl.get("WIKI/GOOGL")
efx = quandl.get("WIKI/EFX") #equifax
mco = quandl.get("WIKI/MCO") #Moody's
   #tru = quandl.get("WIKI/TRU") #transunion
fb['return pct'] = 100*(fb['Adj. Close'].pct_change())
fb['Log Price'] = np.log(fb['Adj. Close'])
fb['returnma'] = pd.rolling_mean(fb['return pct'],30)
goog['return pct'] = 100*(goog['Adj. Close'].pct_change())
goog['Log Price'] = np.log(goog['Adj. Close'])
goog['returnma'] = pd.rolling_mean(goog['return pct'],30)
efx['return pct'] = 100*(efx['Adj. Close'].pct_change())
efx['Log Price'] = np.log(efx['Adj. Close'])
efx['returnma'] = pd.rolling_mean(efx['return pct'],30)
mco['return pct'] = 100*(mco['Adj. Close'].pct_change())
mco['Log Price'] = np.log(mco['Adj. Close'])
mco['returnma'] = pd.rolling_mean(mco['return pct'],30)
marketing = pd.concat([fb['returnma'], goog['returnma'], efx['returnma'], mco['returnma']], axis=1) 
marketing.columns=['fb', 'goog', 'efx', 'mco']
marketing.corr(method='pearson', min_periods=1)

plt.plot(fb['returnma'], label='fb')
plt.plot(goog['returnma'], label='goog')
plt.plot(efx['returnma'], label='efx')
plt.plot(mco['returnma'], label='mco')
plt.xticks(rotation='vertical')
plt.legend()  
plt.plot(fb['Adj. Close'], label='fb')
plt.plot(goog['Adj. Close'], label='goog')
plt.plot(efx['Adj. Close'], label='efx')
plt.plot(mco['Adj. Close'], label='mco')
plt.xticks(rotation='vertical')
plt.legend()  
plt.plot(fb['Log Price'], label='fb')
plt.plot(goog['Log Price'], label='goog')
plt.plot(efx['Log Price'], label='efx')
plt.plot(mco['Log Price'], label='mco')
plt.xticks(rotation='vertical')
plt.legend(loc='best')  



#RETAIL / SERVICES
amzn = quandl.get("WIKI/AMZN") #amazon
wmt = quandl.get("WIKI/WMT") #walmart
cost = quandl.get("WIKI/COST") # Costco
kmx = quandl.get("WIKI/KMX") # carmax
aapl = quandl.get("WIKI/AAPL") # apple
khc = quandl.get("WIKI/KHC") # kraft
ko = quandl.get("WIKI/KO") # cocacola
pg = quandl.get("WIKI/PG") # procter and gamble

amzn['return pct'] = 100*(amzn['Adj. Close'].pct_change())
amzn['returnma'] = pd.rolling_mean(amzn['return pct'],30)
wmt['return pct'] = 100*(wmt['Adj. Close'].pct_change())
wmt['returnma'] = pd.rolling_mean(wmt['return pct'],30)
cost['return pct'] = 100*(cost['Adj. Close'].pct_change())
cost['returnma'] = pd.rolling_mean(cost['return pct'],30)
kmx['return pct'] = 100*(kmx['Adj. Close'].pct_change())
kmx['returnma'] = pd.rolling_mean(kmx['return pct'],30)
aapl['return pct'] = 100*(aapl['Adj. Close'].pct_change())
aapl['returnma'] = pd.rolling_mean(aapl['return pct'],30)
khc['return pct'] = 100*(khc['Adj. Close'].pct_change())
khc['returnma'] = pd.rolling_mean(khc['return pct'],30)
ko['return pct'] = 100*(ko['Adj. Close'].pct_change())
ko['returnma'] = pd.rolling_mean(ko['return pct'],30)
pg['return pct'] = 100*(pg['Adj. Close'].pct_change())
pg['returnma'] = pd.rolling_mean(pg['return pct'],30)
retail = pd.concat([amzn['returnma'], wmt['returnma'], cost['returnma'], kmx['returnma'],aapl['returnma'], khc['returnma'], ko['returnma'], pg['returnma']], axis=1) 
retail.columns=['amzn', 'wmt', 'cost', 'kmx', 'aapl', 'khc', 'ko', 'pg']
retail.corr(method='pearson', min_periods=1)

amzn['Log Price'] = np.log(amzn['Adj. Close'])
wmt['Log Price'] = np.log(wmt['Adj. Close'])
cost['Log Price'] = np.log(cost['Adj. Close'])
kmx['Log Price'] = np.log(kmx['Adj. Close'])
aapl['Log Price'] = np.log(aapl['Adj. Close'])
khc['Log Price'] = np.log(khc['Adj. Close'])
ko['Log Price'] = np.log(ko['Adj. Close'])
pg['Log Price'] = np.log(pg['Adj. Close'])

plt.plot(amzn['Log Price'], label='amzn')
plt.plot(wmt['Log Price'], label='wmt')
plt.plot(cost['Log Price'], label='cost')
plt.plot(kmx['Log Price'], label='kmx')
plt.plot(aapl['Log Price'], label='aapl')
plt.plot(khc['Log Price'], label='khc')
plt.plot(ko['Log Price'], label='ko')
plt.plot(pg['Log Price'], label='pg')
plt.xticks(rotation='vertical')
plt.legend(loc='best') 


#CARS
f = quandl.get("WIKI/F") #ford
gm = quandl.get("WIKI/GM") #gm
#hmc = quandl.get("WIKI/HMC") # honda
tsla = quandl.get("WIKI/TSLA") # tesla
f['return pct'] = 100*(f['Adj. Close'].pct_change())
f['returnma'] = pd.rolling_mean(f['return pct'],30)
gm['return pct'] = 100*(gm['Adj. Close'].pct_change())
gm['returnma'] = pd.rolling_mean(gm['return pct'],30)
tsla['return pct'] = 100*(tsla['Adj. Close'].pct_change())
tsla['returnma'] = pd.rolling_mean(tsla['return pct'],30)
cars = pd.concat([f['returnma'], gm['returnma'], tsla['returnma']], axis=1) 
cars.columns=['f', 'gm', 'tsla']
cars.corr(method='pearson', min_periods=1)

f['Log Price'] = np.log(f['Adj. Close'])
gm['Log Price'] = np.log(gm['Adj. Close'])
tsla['Log Price'] = np.log(tsla['Adj. Close'])

plt.plot(f['Log Price'], label='f')
plt.plot(gm['Log Price'], label='gm')
plt.plot(tsla['Log Price'], label='tsla')
plt.xticks(rotation='vertical')
plt.legend(loc='best') 

#technology
msft = quandl.get("WIKI/MSFT") #Microsoft
intc = quandl.get("WIKI/INTC") #Intel
ibm = quandl.get("WIKI/IBM") # IBM
orcl = quandl.get("WIKI/ORCL") # Oracle

msft['return pct'] = 100*(msft['Adj. Close'].pct_change())
msft['returnma'] = pd.rolling_mean(msft['return pct'],30)
intc['return pct'] = 100*(intc['Adj. Close'].pct_change())
intc['returnma'] = pd.rolling_mean(intc['return pct'],30)
ibm['return pct'] = 100*(ibm['Adj. Close'].pct_change())
ibm['returnma'] = pd.rolling_mean(ibm['return pct'],30)
orcl['return pct'] = 100*(orcl['Adj. Close'].pct_change())
orcl['returnma'] = pd.rolling_mean(orcl['return pct'],30)
tech = pd.concat([msft['returnma'], intc['returnma'], ibm['returnma'], orcl['returnma']], axis=1) 
tech.columns=['msft', 'intc', 'ibm', 'orcl']
tech.corr(method='pearson', min_periods=1)

msft['Log Price'] = np.log(msft['Adj. Close'])
intc['Log Price'] = np.log(intc['Adj. Close'])
ibm['Log Price'] = np.log(ibm['Adj. Close'])
orcl['Log Price'] = np.log(orcl['Adj. Close'])

plt.plot(msft['Log Price'], label='msft')
plt.plot(intc['Log Price'], label='intc')
plt.plot(ibm['Log Price'], label='ibm')
plt.plot(orcl['Log Price'], label='orcl')
plt.xticks(rotation='vertical')
plt.legend(loc='best') 

#communications
vz = quandl.get("WIKI/VZ") #Verizon
t = quandl.get("WIKI/T") #AT&T
tmus = quandl.get("WIKI/TMUS") # tmobile
vz['return pct'] = 100*(vz['Adj. Close'].pct_change())
vz['returnma'] = pd.rolling_mean(vz['return pct'],30)
t['return pct'] = 100*(t['Adj. Close'].pct_change())
t['returnma'] = pd.rolling_mean(t['return pct'],30)

tmus['return pct'] = 100*(tmus['Adj. Close'].pct_change())
tmus['returnma'] = pd.rolling_mean(tmus['return pct'],30)
commun = pd.concat([vz['returnma'], t['returnma'], tmus['returnma']], axis=1) 
commun.columns=['vz', 't', 'tmus']
commun.corr(method='pearson', min_periods=1)

vz['Log Price'] = np.log(vz['Adj. Close'])
t['Log Price'] = np.log(t['Adj. Close'])
tmus['Log Price'] = np.log(tmus['Adj. Close'])

plt.plot(vz['Log Price'], label='vz')
plt.plot(t['Log Price'], label='t')
plt.plot(tmus['Log Price'], label='tmus')
plt.xticks(rotation='vertical')
plt.legend(loc='best') 

#Financials
wfc = quandl.get("WIKI/WFC") #Wellsfargo
cof = quandl.get("WIKI/COF") #capone
bbt = quandl.get("WIKI/BBT") # bbt
trv = quandl.get("WIKI/TRV") # travelers
#lyg = quandl.get("WIKI/LYG") # Lloyds
axp = quandl.get("WIKI/AXP") # american express

wfc['return pct'] = 100*(wfc['Adj. Close'].pct_change())
wfc['returnma'] = pd.rolling_mean(wfc['return pct'],30)
cof['return pct'] = 100*(cof['Adj. Close'].pct_change())
cof['returnma'] = pd.rolling_mean(cof['return pct'],30)
bbt['return pct'] = 100*(bbt['Adj. Close'].pct_change())
bbt['returnma'] = pd.rolling_mean(bbt['return pct'],30)
trv['return pct'] = 100*(trv['Adj. Close'].pct_change())
trv['returnma'] = pd.rolling_mean(trv['return pct'],30)
axp['return pct'] = 100*(axp['Adj. Close'].pct_change())
axp['returnma'] = pd.rolling_mean(axp['return pct'],30)
finance = pd.concat([wfc['returnma'], cof['returnma'], bbt['returnma'], trv['returnma'], axp['returnma']], axis=1) 
finance.columns=['wfc', 'cof', 'bbt', 'trv', 'axp']
finance.corr(method='pearson', min_periods=1)

wfc['Log Price'] = np.log(wfc['Adj. Close'])
cof['Log Price'] = np.log(cof['Adj. Close'])
bbt['Log Price'] = np.log(bbt['Adj. Close'])
trv['Log Price'] = np.log(trv['Adj. Close'])
axp['Log Price'] = np.log(axp['Adj. Close'])

plt.plot(msft['Log Price'], label='msft')
plt.plot(intc['Log Price'], label='intc')
plt.plot(ibm['Log Price'], label='ibm')
plt.plot(orcl['Log Price'], label='orcl')
plt.xticks(rotation='vertical')
plt.legend(loc='best') 

#COMBINE ALL
combined = pd.concat([energy, midstream, airlines, marketing, retail, cars, tech, commun, finance], axis=1) 
combined = energy.join(midstream).join(airlines).join(marketing).join(retail).join(cars).join(tech).join(commun).join(finance)
comb_corr = combined.corr(method='pearson', min_periods=1)

plt.plot(aal['Log Price'], label='aal')
plt.plot(xom['Log Price'], label='xom')
plt.xticks(rotation='vertical')
plt.legend(loc='best')  