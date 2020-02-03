"""
Using the data imported from quandl in get_data the price is predicted
with errors for the next five days, in increments of days.
"""

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA

from get_data.get_data import call_api


def model_arima(n_days, n_predictions):
    """Returns an array of predicted prices for given number of days using
    Quandl API data."""

    data = call_api(n_days)
    df = pd.DataFrame(data)
    
    df = df.drop("Date", axis=1)

    model = ARIMA(df[['Value']], order=(1, 1, 1))
    fitted = model.fit(disp=0)

    # Forecast, standard error, confidence region for a confidence of 95%
    forecast, error, conf = fitted.forecast(n_predictions, alpha=0.05)
    return pd.DataFrame(data={"Prediction": forecast, "Error": error})


