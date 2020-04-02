"""Collect the analysis files from the backend server."""
import numpy as np
import pandas as pd


def get_data():
    """Return boolean and data frame for sell-today and predictions respectively."""
    # DataFrame
    predictions = pd.read_pickle("./get_data/predictions.pkl")
    predictions = predictions.set_index("date")

    # Sell function
    sell_today = np.load("./get_data/sell_today.npy")

    return predictions, sell_today
