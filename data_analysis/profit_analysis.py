"""
Using the predictions created in price_prediction.py the profit margin is analysed
for each prediction.
"""
import pandas as pd
from data_analysis.price_prediction import model_arima

# Information on the Tanker
no_units = 750000
running_cost = 30000

def sell_function(data_points,n_days):
	# Predict 5 days using 2000 data points
	prediction_df = model_arima(data_points, n_days)

	# Calculates the profit for each day predicted taking into account running costs.
	# And compares it with the highest profit so far.
	count = 1
	best_profit = 0
	no_rows = prediction_df.shape[0]
	price = prediction_df.iloc[0]['Prediction']
	pot_profit = no_units*price
	while count < no_rows:
		price = prediction_df.iloc[count]['Prediction']
		profit = no_units*price - running_cost*count
		if pot_profit < profit:
			best_profit = count
			pot_profit = profit
		count += 1
	print('Sell in %i day' % best_profit)

