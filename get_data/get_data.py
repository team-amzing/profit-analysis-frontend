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


def call_api(n_days):
    """
	Calls the api using Michael's key, and returns the last n_days worth of WTI oil price data
	"""
    # Set quandl API key
    quandl.ApiConfig.api_key = "NszGhwY_Qh8Ubj1BWhVt"  # change this to a global constant, maybe even use the team key

    # Get data from the quandl api, then only return the number of days asked for
    data = quandl.get("EIA/PET_RWTC_D", returns="numpy")
    return data[-n_days:]

