import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import requests
import tkinter as tk
import time
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from get_data.scrape import scrape_image_from_url
from get_data.scrape import scrape_data_from_url

# Read in files
SERVER_URL = "http://35.204.193.240/"
predictions, sell_today = scrape_data_from_url( SERVER_URL )
scrape_image_from_url( SERVER_URL )

def create_label(root):
    """ Function to create tkinter label. """

    var = tk.StringVar()
    label = tk.Label(root, textvariable=var, anchor="e", fg="white", bg="black")

    var.set("Default")

    return label, var


def display_graph(root, df, side, title, color):
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

# Configure grid arangment:
num_rows = 3
num_columns = 3

# UI Elements
root = tk.Tk()
root.geometry("580x580")
dateFrame = tk.Frame(root)
dateFrame.pack(fill=tk.X)

# Frame to hold quantative price information:
labelFrame = tk.Frame(root)
labelFrame.pack(side=tk.BOTTOM, fill="both", expand=True)

# Include Logo:
photo = tk.PhotoImage(file="Logo.png")
photo_label = tk.Label(dateFrame, image=photo, fg="white", bg="black").pack(
    side=tk.RIGHT
)

# Display descision:
if sell_today == True:
    decision_string = "SELL"
else:
    decision_string = "DON'T SELL"

# Window setup
todays_price = predictions["predicted_value"][0]
tomorrows_price = predictions["predicted_value"][1]
difference = tomorrows_price - todays_price

# Window
main_window = tk.Label(
    dateFrame,
    text=f"""\n Recommendation: {decision_string}  \n
    Todays Oil Price : {todays_price:.2f} \n
    Predicted price Tomorrow: {tomorrows_price:.2f} \n
    Expected Gain Tomorrow: {difference:.2f} \n""",
    fg="white",
    bg="black",
    relief="raised",
    borderwidth=0,
).pack(fill=tk.X)

# Display Graphs:
###
#dates = [[]] * len(predictions.index)
#for index in range(len(predictions.index)):
#    dates[index] = predictions.index[index].strftime("%Y-%m-%d")

#PLACE THE PNG HERE
graph_image = ImageTk.PhotoImage(Image.open("projection.png"))
image_label = tk.Label(root, image=graph_image).pack()

# Data Grid:
current_date = datetime.datetime.now()

total_num_labels = num_rows * (num_columns * 2)

labels = [[]] * total_num_labels
label_text = [[]] * total_num_labels

label_idx = 0
for column in range(num_columns):
    for row in range(num_rows):

        # Set date columns:
        labels[2 * label_idx], label_text[2 * label_idx] = create_label(labelFrame)

        try:
            date_content = predictions.index[label_idx].strftime("%Y-%m-%d")
        except:
            date_content = "No Data"

        label_text[2 * label_idx].set(f"{date_content}:")

        labels[2 * label_idx].grid(row=row, column=2 * column, sticky="e")

        # Set price columns
        labels[2 * label_idx + 1], label_text[2 * label_idx + 1] = create_label(
            labelFrame
        )

        try:
            price_value = predictions["predicted_value"][label_idx]
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
root.mainloop()
