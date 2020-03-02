import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests
import tkinter as tk
import time

from bs4 import BeautifulSoup
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from data_analysis.price_prediction import model_arima
from get_data.get_data import call_api


def sell_function(data_points, n_days):
    """ Predict 5 days using 2000 data points """

    prediction_df = model_arima(data_points, n_days)

    # Calculates the profit for each day predicted taking into account running
    # costs and compares it with the highest profit so far.
    profit_array = [None] * (n_days + 1)

    for count in range(n_days):
        price = prediction_df.iloc[count]["Prediction"]
        profit_array[count + 1] = price

    return profit_array


def showCurrentPrice():
    """ Webscrapes and returns current market price for oil """

    page = requests.get(
        "https://markets.businessinsider.com/commodities/oil-price?type=wti"
    )
    soup = BeautifulSoup(page.text, "html.parser")
    currentPrices = soup.find(class_="push-data")
    price = str(currentPrices.next)

    return price


def createLabel(root):
    """ Function to create tkinter label. """

    var = tk.StringVar()
    label = tk.Label(root, textvariable=var, anchor="e", fg="white", bg="black")

    var.set("Default")

    return label, var

def diplayGraph(root, df, side, title, color):
    """ Displays a graph on a tkinter frame """

    figure = plt.Figure(figsize=(5, 4), dpi=100)
    figure.patch.set_facecolor("black")
    ax = figure.add_subplot(111)
    line = FigureCanvasTkAgg(figure, root)
    line.get_tk_widget().pack(side= side, fill=tk.BOTH)
    df.plot(kind="line", legend=True, ax=ax, color=color, marker="o", fontsize=10)
    ax.set_facecolor("black")
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.grid(b=True, which="major", color="#666666", linestyle="-")
    ax.spines["top"].set_color("white")
    ax.spines["bottom"].set_color("white")
    ax.spines["left"].set_color("white")
    ax.spines["right"].set_color("white")
    ax.tick_params(axis="x", colors="white")
    ax.tick_params(axis="y", colors="white")
    ax.set_title(title, color="white")

    return figure, ax, line



def tick():
    """ Tick function which runs each tkinter tick """

    global time1
    # get the current local time from the PC
    time2 = time.strftime("%H:%M:%S")
    # if time string has changed, update it
    if time2 != time1:
        time1 = time2
        timeLabel.config(text=time2)
    # calls itself every 200 milliseconds
    # to update the time display as needed
    # could use >200 ms, but display gets jerky
    timeLabel.after(200, tick)


# Variables:

num_days_ahead_to_predict = 7
num_days_previous_to_show = 10
num_days_to_train_on = 2000

# Configure grid arangment:
num_rows = 4
num_columns = 4

# Make prediction:
prediction_df = model_arima(num_days_to_train_on, num_days_ahead_to_predict)
prediction_df = prediction_df.rename(columns={"Prediction": "Value"})

# Call real data from API:
data = pd.DataFrame(call_api(num_days_previous_to_show))
data = data.append(prediction_df)
data = data.reset_index(drop=True)

# Add dates to dataframe predicted rows:
# TODO Find a more elegant soloution for this mess - Michael
last = None
recent_date_check = 1
most_recent_date = None
for i, row in data.iterrows():
    if pd.isnull(row["Date"].to_numpy()):
        data.loc[i, "Date"] = last + datetime.timedelta(days=1)
        row["Date"] = last + datetime.timedelta(days=1)

        if recent_date_check == 1:
            most_recent_date = row["Date"]
            recent_date_check = 0

    if i != 0:
        last = row["Date"]

price_df = pd.DataFrame(data, columns=["Date", "Value"])
price_df = price_df[["Date", "Value"]].groupby("Date").sum()

# Make decision on whether to sell or not:
decision = 1

currentP = showCurrentPrice()
sixDayPrediction = sell_function(num_days_to_train_on, num_days_ahead_to_predict)
sixDayPrediction[0] = currentP
TomorrowPred = sixDayPrediction[1]
difference = 0
decision = 0

if TomorrowPred > float(sixDayPrediction[0]):
    difference = TomorrowPred - float(sixDayPrediction[0])
    decision = 0
else:
    difference = float(sixDayPrediction[0]) - TomorrowPred
    decision = 1
difference = str(round(difference, 2))

# Calculate Profits:
profits = [[]] * (num_days_ahead_to_predict + 1)
dates = [[]] * (num_days_ahead_to_predict + 1)

for day in range(num_days_ahead_to_predict + 1):
    profits[day] = float(sixDayPrediction[day]) - float(currentP)

profit_df = pd.DataFrame(profits, columns=["Profit"])
profit_df["Date"] = dates

last = most_recent_date - datetime.timedelta(days=2)
for i, row in profit_df.iterrows():
    profit_df.loc[i, "Date"] = last + datetime.timedelta(days=1)
    row["Date"] = last + datetime.timedelta(days=1)
    last = row["Date"]

profit_df = profit_df[["Date", "Profit"]].groupby("Date").sum()

# UI Elements
root = tk.Tk()

dateFrame = tk.Frame(root)
dateFrame.pack(fill=tk.X)
timeFrame = tk.Frame(root)
timeFrame.pack(fill=tk.X)
time1 = ""

# Frame to hold quantative price information:
labelFrame = tk.Frame(root)
labelFrame.pack(side=tk.BOTTOM, fill="both", expand=True)

# Include Logo:
photo = tk.PhotoImage(file="./frontend/Logo.png")
photo_label = tk.Label(dateFrame, image=photo, fg="white", bg="black").pack(
    side=tk.RIGHT
)

# Display descision:

six_day_prediction_string = str(sixDayPrediction[0])
tommorow_prediction_string = str(round(TomorrowPred, 2))

if decision == 1:
    decision_string = "SELL"
else:
    decision_string = "DON'T SELL"

main_window = tk.Label(
    root,
    text=f"""\n Recommendation: {decision_string}  \n
    Todays Oil Price : {six_day_prediction_string} \n
    Predicted price Tomorrow: {tommorow_prediction_string} \n
    Expected Gain Tomorrow: {difference} \n""",
    fg="white",
    bg="black",
    relief="raised",
    borderwidth=5,
    font=("Times 32", 16),
).pack()

# Display Graphs:

dates = [[]] * len(profit_df.index)
for index in range(len(profit_df.index)):
    dates[index] = profit_df.index[index].strftime("%Y-%m-%d")

price_figure, price_ax, price_line = diplayGraph(root, price_df, tk.LEFT, "Oil Price", "r")
profit_figure, profit_ax, profit_line = diplayGraph(root, profit_df, tk.RIGHT, "Predicted Profit", "g")
profit_ax.set_xticklabels(dates, rotation=35, fontsize=10)

# Data Grid:
current_date = datetime.datetime.now()

dateLabel = tk.Label(dateFrame, text=current_date.strftime("%x"), fg="white")
timeLabel = tk.Label(dateFrame, text=current_date.strftime("%X"), fg="white")

dateLabel.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)
timeLabel.pack(side=tk.LEFT, anchor=tk.N, padx=5, pady=5)

total_num_labels = num_rows * (num_columns * 2)

labels = [[]] * total_num_labels
label_text = [[]] * total_num_labels

label_idx = 0
for column in range(num_columns):
    for row in range(num_rows):

        # Set date columns:
        labels[2 * label_idx], label_text[2 * label_idx] = createLabel(labelFrame)

        try:
            date_content = data["Date"][label_idx].strftime("%Y-%m-%d")
        except:
            date_content = "No Data"

        label_text[2 * label_idx].set(f"{date_content}:")

        labels[2 * label_idx].grid(row=row, column=2 * column, sticky="e")

        # Set price columns
        labels[2 * label_idx + 1], label_text[2 * label_idx + 1] = createLabel(
            labelFrame
        )

        try:
            price_value = data["Value"][label_idx]
            price_content = f"{price_value:.2f}"
        except:
            price_content = "VALUE_MISSING"

        label_text[2 * label_idx + 1].set(f"{price_content}")

        labels[2 * label_idx + 1].grid(row=row, column=2 * column + 1, sticky="w")

        label_idx += 1

    tk.Grid.columnconfigure(labelFrame, 2 * column, weight=1)
    tk.Grid.columnconfigure(labelFrame, 2 * column + 1, weight=1)

# painting all frames
root.configure(background="black")
labelFrame.configure(background="black")
dateFrame.configure(background="black")
timeFrame.configure(background="black")
dateLabel.configure(background="black")
timeLabel.configure(background="black")
tick()
root.mainloop()
