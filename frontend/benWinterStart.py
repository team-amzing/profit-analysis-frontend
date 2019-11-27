
import tkinter as tk
import datetime
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

Data1 = {'Day': ['Tuesday','Wednesday','Thursday','Friday','Today','Tomorrow','Wednesday','Thursday','Friday'],
        'Oil_Price': [55.5,60.1,62.9,61.7,63.1,62.4,62.1,59.7,63.9]
       }
  
df1 = DataFrame(Data1,columns=['Day','Oil_Price'])
df1 = df1[['Day', 'Oil_Price']].groupby('Day').sum()

Data2 = {'Day': ['Tuesday','Wednesday','Thursday','Friday','Today','Tomorrow','Wednesday','Thursday','Friday'],
        'Profit': [6.2,5.7,5.9,4.9,7.2,8.1,7.4,4.5,4.8]
       }
  
df2 = DataFrame(Data2,columns=['Day','Profit'])
df2 = df2[['Day', 'Profit']].groupby('Day').sum()

root= tk.Tk()
 
dateFrame = tk.Frame(root)
dateFrame.pack(fill=tk.X)
timeFrame = tk.Frame(root)
timeFrame.pack(fill=tk.X)
decision = 1
if decision == 1:
    decisionLabel = tk.Label(dateFrame, text="SELL SELL SELL", fg="green",font =("Times 32",40)).pack()
else:
    decisionLabel = tk.Label(dateFrame, text="We advise you not to sell today", fg="red",font =("Times 32",40)).pack()
if decision ==1:
	main_window = tk.Label(root, text="\n Recommendation: SELL   \n \n Todays Oil Price : insert value here \n \n Predicted price Tomorrow:  value \n \n Epected Gain Tomorrow: +-value \n", fg = 'white',bg = 'black', relief = "raised", borderwidth = 5, font =("Times 32",16)).pack()
else:
	main_window = tk.Label(root, text="\n Recommendation: DIM SELL   \n \n Todays Oil Price : insert value here \n \n Predicted price Tomorrow:  value \n \n Epected Gain Tomorrow: +-value \n", fg = 'white',bg = 'black', relief = "raised", borderswidth = 5, font =("Times 32",16)).pack()

figure1 = plt.Figure(figsize=(5,4), dpi=100)
ax1 = figure1.add_subplot(111)
line1 = FigureCanvasTkAgg(figure1, root)
line1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

df1.plot(kind='line', legend=True, ax=ax1, color='r', marker='o', fontsize=10)
ax1.set_title('Day Vs. Oil Price')

figure2 = plt.Figure(figsize=(5,4), dpi=100)
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, root)
line2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
df2.plot(kind='line', legend=True, ax=ax2, color='g',marker='x', fontsize=10)
ax2.set_title('Day Vs. Profit')

x = datetime.datetime.now()

dateLabel = tk.Label(dateFrame, text=x.strftime("%x"), fg="black")
timeLabel = tk.Label(timeFrame, text=x.strftime("%X"), fg="black")

decision = 1
if decision == 1:
    decisionLabel = tk.Label(dateFrame, text="SELL SELL SELL", fg="green")
else:
    decisionLabel = tk.Label(dateFrame, text="We advise you not to sell today", fg="red")

dateLabel.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)
timeLabel.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)

root.mainloop()
