"""
WIT oil price data is acquired from the Quandl API for use by the data_analysis module.
"""
import numpy as np
import matplotlib.pyplot as plt
import quandl
from datetime import datetime
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import os

from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()  # <-- Something about you having to explicity register your datatime converters or matplotlib has a fit.


def validateDateString(date_string):
    """
	Validates whether date_string is in the correct format.
	"""

    result = None

    try:
        datetime.strptime(date_string, "%Y%m%d")
        result = True
    except ValueError:
        result = False
    return result

def call_api(n_days):
	"""
	Calls the api using Michael's key, and returns n_days worth of WTI price data
	"""
	# Set quandl API key
	quandl.ApiConfig.api_key = "NszGhwY_Qh8Ubj1BWhVt" # change this to a global constant, maybe even use the team key

	# Get current date and convert to string:
	now = datetime.now()
	string_date = now.strftime("%Y%m%d")

	# Searches working directory for date oil price files and retreives dates:
	directory_contents = os.listdir()
	dates = [0]
	for item in directory_contents:

	    split = item.split(".")
	    extension = split[-1]
	    name = split[0][0:10]
	    date = split[0][11:19] # not actually always a date, hence the validateDateString function

	    extension_check = extension == "npy"
	    name_check = name == "oil_prices"
	    date_check = validateDateString(date)

	    if extension_check & name_check & date_check:
	        dates.append(int(date))

	# If latest oil price file has been created today load it, else create a new file:
	data = None
	if int(string_date) > np.max(dates):
	    data = quandl.get("EIA/PET_RWTC_D", returns="numpy")
	    np.save("oil_prices_{}".format(string_date), data)
	else:
	    data = np.load("oil_prices_{}.npy".format(string_date), data)
	return data[-n_days:] #easiest way is just to splice the array only taking the number of days you want
