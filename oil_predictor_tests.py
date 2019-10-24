import numpy as np
import matplotlib.pyplot as plt 
import quandl 
from datetime import datetime
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import os

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters() #<-- Something about you having to explicity register your datatime converters or matplotlib has a fit.

def validateDateString(date_string):
	"""
	Validates whether date_string is in the correct format.
	"""

	result = None

	try:
		datetime.strptime(date_string, '%Y%m%d')
		result = True
	except ValueError:
		result = False
	return result

#Set quandl API key
quandl.ApiConfig.api_key = "NszGhwY_Qh8Ubj1BWhVt"

#Get current date and convert to string:
now         = datetime.now()        
string_date = now.strftime("%Y%m%d")

#Searches working directory for date oil price files and retreives dates:
directory_contents = os.listdir()
dates = []
for item in directory_contents:

	split     = item.split('.') 
	extension = split[-1]
	name      = split[0][0:10]
	date      = split[0][11:19]

	extension_check = (extension == 'npy')
	name_check      = (name == 'oil_prices')
	date_check      = validateDateString(date)

	if ( extension_check & name_check & date_check):
		dates.append(int(date))

#If latest oil price file has been created today load it, else create a new file:
data = None
if (int(string_date) > np.max(dates)):
	data = quandl.get("EIA/PET_RWTC_D", returns = 'numpy')
	np.save('oil_prices_{}'.format(string_date), data)
else:
	data = np.load('oil_prices_{}.npy'.format(string_date), data)

plt.plot(data['Date'], data['Value'])
plt.savefig('test_oil_prices.png')

#Fit ARIMA model to the data 
model = ARIMA(data['Value'], order=(5,1,0))
model_fit = model.fit(disp=0)
print(model_fit.summary())

# plot residual errors
residuals = pd.DataFrame(model_fit.resid)
residuals.plot()
plt.savefig('residuals_1')
residuals.plot(kind='kde')
plt.savefig('residuals_2')
print(residuals.describe())

## Predictions:

X = data['Value']
size = int(len(X) * 0.66)
train, test = X[0:size], X[size:len(X)]

history = [x for x in train]
predictions = list()
for t in range(len(test)):
	model = ARIMA(history, order=(5,1,0))
	model_fit = model.fit(disp=0)
	output = model_fit.forecast()
	yhat = output[0]
	predictions.append(yhat)
	obs = test[t]
	history.append(obs)
	print('%s, Predicted = %f, Expected = %f, Difference = %f' % (str(data['Date'][t + size])[0:10], yhat, obs, (yhat-obs)) )
