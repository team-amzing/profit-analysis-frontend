
import tkinter as tk
import datetime
from pandas import DataFrame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def createLabel(root):
  # Function to create tkinter label.
  var   = tk.StringVar()
  label = tk.Label( root, textvariable=var, anchor="e")

  var.set("Default")

  return label, var

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
TP = 55
root= tk.Tk()
 
dateFrame = tk.Frame(root)
dateFrame.pack(fill=tk.X)
timeFrame = tk.Frame(root)
timeFrame.pack(fill=tk.X)

#Frame to hold quantative price information:
labelFrame = tk.Frame(root)
labelFrame.pack(side = tk.BOTTOM, fill='both', expand=True)

decision = 1
photo = tk.PhotoImage(file='Logo.png')
photo_label = tk.Label(root, image =photo).pack(side=tk.TOP)

if decision == 1:
    decisionLabel = tk.Label(dateFrame, text="SELL SELL SELL", fg="green",font =("Times 32",40)).pack(side = tk.TOP)
else:
    decisionLabel = tk.Label(dateFrame, text="We advise you not to sell today", fg="red",font =("Times 32",40)).pack(side = tk.TOP)
if decision ==1:
	main_window = tk.Label(root, text="\n Recommendation: SELL   \n  Todays Oil Price : insert value here \n  Predicted price Tomorrow:  value \n  Epected Gain Tomorrow: +-value \n", fg = 'white',bg = 'black', relief = "raised", borderwidth = 5, font =("Times 32",16)).pack()
else:
	main_window = tk.Label(root, text="\n Recommendation: DIM SELL   \n  Todays Oil Price : insert value here \n  Predicted price Tomorrow:  value \n  Epected Gain Tomorrow: +-value \n", fg = 'white',bg = 'black', relief = "raised", borderswidth = 5, font =("Times 32",16)).pack()

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

    label_text[2*label_idx].set("{}:".format(Data1['Day'][label_idx]))
    labels[2*label_idx]    .grid(row=row,column=2*column, sticky='e')

    #Set price columns
    labels[2*label_idx + 1], label_text[2*label_idx + 1] = createLabel(labelFrame)

    label_text[2*label_idx + 1].set("{}".format(Data1['Oil_Price'][label_idx]))
    labels    [2*label_idx + 1].grid(row=row,column= 2*column + 1, sticky='w')

    label_idx += 1

  tk.Grid.columnconfigure(labelFrame, 2*column, weight=1)
  tk.Grid.columnconfigure(labelFrame, 2*column + 1, weight=1)

root.mainloop()
