"""
Using the data imported from quandl in get_data the price is predicted
with errors for the next five days, in increments of days.
"""

import numpy as np
from statsmodels.tsa.arima_model import ARIMA


from get_data.get_data import call_api


def model_arima():
    """Returns an array of predicted prices for given number of days using
    Quandl API data."""

    data = call_api(N_DAYS)

    pass
