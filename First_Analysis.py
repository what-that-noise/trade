# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 16:16:33 2017

@author: aletwhittington
"""

import quandl
import matplotlib.pyplot as plt

quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"


mult_data = quandl.get(["WIKI/CHK.1", "WIKI/IBM.1"], start_date="2008-01-01", end_date="2015-12-31", collapse="monthly", transform="rdiff")

mult_data.plot.hist(alpha=0.3)