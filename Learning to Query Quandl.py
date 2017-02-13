# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 14:55:49 2017

@author: aletwhittington
"""

import quandl
import matplotlib.pyplot as plt

quandl.ApiConfig.api_key = "Vm3hGqA7K_chXo6DfTqx"
fb = quandl.get("WIKI/FB")
goog = quandl.get("WIKI/GOOG")

""" Query - Monthly data, first coloumn of dataset, % change """
data = quandl.get("WIKI/CHK.1", start_date="2008-01-01", end_date="2014-12-31", collapse="monthly", transform="rdiff")

""" Query - Multiple Companies, Monthly data, first coloumn of dataset, % change """
merge_data = quandl.get(["WIKI/CHK.1", "WIKI/GOOG", "WIKI/FB.1"], start_date="2008-01-01", end_date="2014-12-31", collapse="monthly", transform="rdiff")

chk = merge_data[['WIKI/CHK - Open']]

chk.plot.hist()

mult_data = quandl.get(["WIKI/CHK.1", "WIKI/IBM.1"], start_date="2008-01-01", end_date="2015-12-31", collapse="monthly", transform="rdiff")

mult_data.plot.hist(alpha=0.5)
"""
QUERY PARAMETERS

Parameter	Req’d	Type	Values	Description
database_code	yes	string		Code identifying the database to which the dataset belongs.
dataset_code	yes	string		Code indentifying the dataset.
limit	no	int		Use limit=n to get the first n rows of the dataset. Use limit=1 to get just the latest row.
column_index	no	int		Request a specific column. Column 0 is the date column and is always returned. Data begins at column 1.
start_date	no	string	yyyy-mm-dd	Retrieve data rows on and after the specified start date.
end_date	no	string	yyyy-mm-dd	Retrieve data rows up to and including the specified end date.
order	no	string	asc 
desc	Return data in ascending or descending order of date. Default is “desc”.
collapse	no	string	none 
                            daily 
                            weekly 
                            monthly 
                            quarterly 
                            annual	Change the sampling frequency of the returned data. Default is “none” i.e. data is returned in its original granularity.
transform	no	string	none 
                            diff 
                            rdiff 
                            rdiff_from
                            cumul 
                            normalize	Perform elementary calculations on the data prior to downloading. Default is “none”. Calculation options are described below
"""

"""
Transformations

Name	Effect	Formula
none	no effect	y"[t] = y[t]
diff	row-on-row change	y"[t] = y[t] – y[t-1]
rdiff	row-on-row % change	y"[t] = (y[t] – y[t-1]) / y[t-1]
rdiff_from	latest value as % increment	y"[t] = (y[latest] – y[t]) / y[t]
cumul	cumulative sum	y"[t] = y[0] + y[1] + … + y[t]
normalize	scale series to start at 100	y"[t] = y[t] ÷ y[0] * 100
Note that in the above table, y[0] referes to the starting date specified by start_date or limit, and not the starting date of the underlying raw dataset. Similarly, y[latest] refers to the latest date specified by end_date.


"""

