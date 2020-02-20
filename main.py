import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import tkinter as tk
import time

from bs4 import BeautifulSoup
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame

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

# Configure grid arangment:
num_rows = 4
num_columns = 3

# Make prediction:
prediction_df = model_arima(2000, 5)
prediction_df = prediction_df.rename(columns={"Prediction": "Value"})

# Call real data from API:
data = DataFrame(call_api(10))
data = data.append(prediction_df)
data = data.reset_index(drop=True)

# Add dates to dataframe predicted rows:
# TODO Find a more elegant soloution for this mess - Michael
last = None
for i, row in data.iterrows():
    if pd.isnull(row["Date"].to_numpy()):
        data.loc[i, "Date"] = last + datetime.timedelta(days=1)
        row["Date"] = last + datetime.timedelta(days=1)
    if i != 0:
        last = row["Date"]

df1 = DataFrame(data, columns=["Date", "Value"])
df1 = df1[["Date", "Value"]].groupby("Date").sum()

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

# Make decision on whether to seel or not:
decision = 1

currentP = showCurrentPrice()
sixDayPrediction = sell_function(2000, 6)
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

figure1 = plt.Figure(figsize=(5, 4), dpi=100)
figure1.patch.set_facecolor("black")
ax1 = figure1.add_subplot(111)
line1 = FigureCanvasTkAgg(figure1, root)
line1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
df1.plot(kind="line", legend=True, ax=ax1, color="r", marker="o", fontsize=10)
ax1.set_facecolor("black")
ax1.grid(b=True, which="major", color="#666666", linestyle="-")
ax1.spines["top"].set_color("white")
ax1.spines["bottom"].set_color("white")
ax1.spines["left"].set_color("white")
ax1.spines["right"].set_color("white")
ax1.tick_params(axis="x", colors="white")
ax1.tick_params(axis="y", colors="white")
ax1.set_title("Date Vs. Oil Price", color="white")

Data2 = {
    "Date": [
        "Today",
        "Tomorrow",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
    ],
    "Profit": [
        float(sixDayPrediction[0]) - float(currentP),
        float(sixDayPrediction[1]) - float(currentP),
        float(sixDayPrediction[2]) - float(currentP),
        float(sixDayPrediction[3]) - float(currentP),
        float(sixDayPrediction[4]) - float(currentP),
        float(sixDayPrediction[5]) - float(currentP),
        float(sixDayPrediction[6]) - float(currentP),
    ],
}
df2 = DataFrame(Data2, columns=["Date", "Profit"])

figure2 = plt.Figure(figsize=(5, 4), dpi=100)
figure2.patch.set_facecolor("black")
ax2 = figure2.add_subplot(111)
line2 = FigureCanvasTkAgg(figure2, root)
line2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)
df2.plot(kind="line", legend=True, ax=ax2, color="g", marker="x", fontsize=10)
ax2.set_facecolor("black")
ax2.grid(b=True, which="major", color="#666666", linestyle="-")
ax2.spines["top"].set_color("white")
ax2.set_xticklabels(
    ["Today", "Tomorrow", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    fontsize=6,
)
ax2.spines["bottom"].set_color("white")
ax2.spines["left"].set_color("white")
ax2.spines["right"].set_color("white")
ax2.tick_params(axis="x", colors="white")
ax2.tick_params(axis="y", colors="white")
ax2.set_title("Date Vs. Profit", color="white")

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

        # Set day columns:
        labels[2 * label_idx], label_text[2 * label_idx] = createLabel(labelFrame)

        label_text[2 * label_idx].set("{}:".format(data["Date"][label_idx]))
        labels[2 * label_idx].grid(row=row, column=2 * column, sticky="e")

        # Set price columns
        labels[2 * label_idx + 1], label_text[2 * label_idx + 1] = createLabel(
            labelFrame
        )

        label_text[2 * label_idx + 1].set("{}".format(data["Value"][label_idx]))
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
