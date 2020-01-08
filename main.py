import tkinter as tk
import datetime
import time
import pandas as pd
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data_analysis.price_prediction import model_arima
from get_data.get_data import call_api

def createLabel(root):
  # Function to create tkinter label.
  var   = tk.StringVar()
  label = tk.Label( root, textvariable=var, anchor="e")

  var.set("Default")

  return label, var

#Dummy Data still:
Data2 = {'Date': ['Tuesday','Wednesday','Thursday','Friday','Today','Tomorrow','Wednesday','Thursday','Friday'],
        'Profit': [6.2,5.7,5.9,4.9,7.2,8.1,7.4,4.5,4.8]
       }

prediction_df = model_arima(2000, 5)
prediction_df = prediction_df.rename(columns = {"Prediction" :  "Value" })
data          = DataFrame(call_api(10))

data = data.append(prediction_df)
data = data.reset_index(drop=True)

#Apologies this is a bit of a mess:
last = None
for i, row in data.iterrows():
	if ((np.isnan(row['Date'].to_numpy()))):
		data.loc[i,'Date'] = last + datetime.timedelta(days=1)
		row['Date']        = last + datetime.timedelta(days=1)
	if (i != 0):
		last = row['Date']
  
df1 = DataFrame(data,columns=['Date','Value'])
df1 = df1[['Date', 'Value']].groupby('Date').sum()

df2 = DataFrame(Data2,columns=['Date','Profit'])
df2 = df2[['Date', 'Profit']].groupby('Date').sum()
TP = 55
root= tk.Tk()
 
dateFrame = tk.Frame(root)
dateFrame.pack(fill=tk.X)
timeFrame = tk.Frame(root)
timeFrame.pack(fill=tk.X)
time1 = ''

#Frame to hold quantative price information:
labelFrame = tk.Frame(root)
labelFrame.pack(side = tk.BOTTOM, fill='both', expand=True)

decision = 1

photo = tk.PhotoImage(file='./frontend/Logo.png')
#Line underneath for ben
#photo = tk.PhotoImage(file='/Users/benwinter/Documents/Arima/Front End/Logo.png/')
photo_label = tk.Label(dateFrame, image =photo).pack(side=tk.RIGHT)

#if decision == 1:
   # decisionLabel = tk.Label(dateFrame, text="SELL SELL SELL", fg="green",font =("Times 32",40)).pack()
#else:
    #decisionLabel = tk.Label(dateFrame, text="We advise you not to sell today", fg="red",font =("Times 32",40)).pack(side = tk.TOP)
if decision ==1:
	main_window = tk.Label(root, text="\n Recommendation: SELL   \n  Todays Oil Price : insert value here \n  Predicted price Tomorrow:  value \n  Epected Gain Tomorrow: +-value \n", fg = 'white',bg = 'black', relief = "raised", borderwidth = 5, font =("Times 32",16)).pack()
else:
	main_window = tk.Label(root, text="\n Recommendation: DIM SELL   \n  Todays Oil Price : insert value here \n  Predicted price Tomorrow:  value \n  Epected Gain Tomorrow: +-value \n", fg = 'white',bg = 'black', relief = "raised", borderswidth = 5, font =("Times 32",16)).pack()

figure1 = plt.Figure(figsize=(5,4), dpi=100)
ax1 = figure1.add_subplot(111)
line1 = FigureCanvasTkAgg(figure1, root)
line1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

df1.plot(kind='line', legend=True, ax=ax1, color='r', marker='o', fontsize=10)
ax1.set_title('Date Vs. Oil Price')

figure2 = plt.Figure(figsize=(5,4), dpi=100)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, root)
line2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
df2.plot(kind='line', legend=True, ax=ax2, color='g',marker='x', fontsize=10)
ax2.set_title('Date Vs. Profit')

x = datetime.datetime.now()

dateLabel = tk.Label(dateFrame, text=x.strftime("%x"), fg="black")
timeLabel = tk.Label(dateFrame, text=x.strftime("%X"), fg="black")

dateLabel.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)
timeLabel.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)
#dateLabel.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)

#Configure grid arangment
num_rows = 3
num_columns = 2

total_num_labels = num_rows*(num_columns * 2)

labels     = [[]]*total_num_labels
label_text = [[]]*total_num_labels

label_idx = 0
for column in range(num_columns):
  for row in range(num_rows):

    #Set day columns:
    labels[2*label_idx], label_text[2*label_idx] = createLabel(labelFrame)

    label_text[2*label_idx].set("{}:".format(data['Date'][label_idx]))
    labels[2*label_idx]    .grid(row=row,column=2*column, sticky='e')

    #Set price columns
    labels[2*label_idx + 1], label_text[2*label_idx + 1] = createLabel(labelFrame)

    label_text[2*label_idx + 1].set("{}".format(data['Value'][label_idx]))
    labels    [2*label_idx + 1].grid(row=row,column= 2*column + 1, sticky='w')

    label_idx += 1

  tk.Grid.columnconfigure(labelFrame, 2*column, weight=1)
  tk.Grid.columnconfigure(labelFrame, 2*column + 1, weight=1)

def tick():
    global time1
    # get the current local time from the PC
    time2 = time.strftime('%H:%M:%S')
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        timeLabel.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    timeLabel.after(200, tick)

tick()
root.mainloop()
