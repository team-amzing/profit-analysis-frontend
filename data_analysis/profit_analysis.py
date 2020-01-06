"""
Using the predictions created in price_prediction.py the profit margin is analysed
for each prediction.
"""

from data_analysis.price_prediction import model_arima

# Predict 5 days using 2000 data points
prediction_df = model_arima(2000, 5)
