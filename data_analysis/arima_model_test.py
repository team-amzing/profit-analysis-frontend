from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA

from get_data.get_data import call_api

data = call_api(2000)
df = pd.DataFrame(data)
df = df.drop("Date", axis=1)
size_index = int(len(df) * 0.9)
train = df.values[:size_index]
test = df.values[size_index:]

model = ARIMA(train, order=(1, 1, 1))
fitted = model.fit(disp=0)

# Forecast, standard error, confidence region for a confidence of 95%
fc, se, conf = fitted.forecast(len(test), alpha=0.05)

# Create pandas series
fc_series = pd.Series(fc, index=np.arange(size_index, len(df)))
lower_series = pd.Series(conf[:, 0], index=np.arange(size_index, len(df)))
upper_series = pd.Series(conf[:, 1], index=np.arange(size_index, len(df)))
test_series = pd.Series(test.flatten(), index=np.arange(size_index, len(df)))

plt.figure(figsize=(12, 5), dpi=100)
plt.plot(train, label="training")
plt.plot(test_series, label="actual")
plt.plot(fc_series, label="forecast")
plt.fill_between(
    lower_series.index,
    lower_series,
    upper_series,
    color="k",
    alpha=0.15,
    label="95% HDI",
)
plt.title("Forecast vs Actuals")
plt.legend(loc="upper left", fontsize=8)
plt.show()


def forecast_accuracy(forecast, actual):
    """Metrics for measuring accuracy of model."""
    # Mean Absolute Percentage Error
    mape = np.mean(np.abs(forecast - actual) / np.abs(actual))
    # Mean Error
    me = np.mean(forecast - actual)
    # Mean Absolute Error
    mae = np.mean(np.abs(forecast - actual))
    # Mean Percentage Error
    mpe = np.mean((forecast - actual) / actual)
    # Root Mean Squared Error
    rmse = np.mean((forecast - actual) ** 2) ** 0.5
    # Correlation between the Actual and the Forecast
    corr = np.corrcoef(forecast, actual)[0, 1]
    mins = np.amin(np.hstack([forecast[:, None], actual[:, None]]), axis=1)
    maxs = np.amax(np.hstack([forecast[:, None], actual[:, None]]), axis=1)
    # Minmax error
    minmax = 1 - np.mean(mins / maxs)
    return {
        "mape": mape,
        "me": me,
        "mae": mae,
        "mpe": mpe,
        "rmse": rmse,
        "corr": corr,
        "minmax": minmax,
    }


forecast_accuracy(fc, test.flatten())
