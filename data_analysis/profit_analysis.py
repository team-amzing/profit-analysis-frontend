"""
Using the predictions created in price_prediction.py the profit margin is analysed
for each prediction.
"""

from data_analysis.price_prediction import model_arima
import pandas as pd
# Information on the Tanker
no_units = 750000
running_cost = 30000

def sell_function(data_points,n_days):
	# Predict 5 days using 2000 data points
	prediction_df = model_arima(data_points, n_days)
	print(prediction_df)
	#prediction_df = pd.DataFrame(data={'Prediction':[50, 55, 70],'Error':[1.2, 1.4, 1.9]})

	# Calculates the profit for each day predicted taking into account running costs.
	# And compares it with the highest profit so far.
	count = 1
	best_profit = 0
	price = prediction_df.iloc[0]['Prediction']
	pot_profit = no_units*price
	profit_array = [pot_profit]
	while count < n_days:
		price = prediction_df.iloc[count]['Prediction']
		profit = no_units*price - running_cost*count
		profit_array.append(profit)
		if pot_profit < profit:
			best_profit = count
			pot_profit = profit
		count += 1
	if best_profit == 0: 
		result = 'Sell today'
	elif best_profit == 1:
		result = 'Sell tomorrow'
	else:
		result = 'Sell in ' + str(best_profit) + ' days'
	return result, profit_array;
