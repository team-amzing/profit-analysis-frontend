"""
A script to scrape the server for the results of our backend, and output these results
in a way that they can be simply read by the frontend GUI
"""


from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import numpy as np
import pandas as pd

url_with_data = "http://35.204.193.240/"


def scrape_data_from_url(url):
    """
    A function to scrape data from a given url, and return the data as numpy arrays
    """
    # Declare arrays where the data will be stored
    dates = []
    pred_vals = []
    errors = []

    # Open the url, save the html, and the close link to url
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    # Parse this html
    page_soup = soup(page_html, "html.parser")  # Second arg is a bs4 keyword
    table = page_soup.find("table")
    rows = table.find_all("tr")
    i = 0  # Will let use save headers seperately
    # Now I have islated the row, loop through the rows and save the data, headers seperately!
    for raw_row in rows:
        if i == 0:
            head = raw_row.find_all("th")
            header1 = str(head[0]).strip("</th>")
            header2 = str(head[1]).strip("</th>")
            header3 = str(head[2]).strip("</th>")
            i = 1
            pass  # First row is the headers
        else:
            row = raw_row.find_all("td")
            dates.append( str( row[0] ).strip("</td>"))
            pred_vals.append( float( str( row[1] ).strip("</td>")))
            errors.append( float( str( row[2] ).strip("</td>")))

    df = pd.DataFrame({
                        header1 : dates,
                        header2 : pred_vals,
                        header3 : errors
                        })

    df = df.set_index("date")
    should_sell_string = str(page_soup.find_all("h2")[1]).strip(
        "</h2>"
    )  # This just isolates the line that says 'Should sell today? True' (or False)
    true_or_false = should_sell_string[-5:]  # Find if it says true or false
    if true_or_false == "False":
        sell = 0
    elif true_or_false == " True":
        sell = 1
    else:
        printf("Can't find if you want to sell or not")

    return df, sell


df, sell = scrape_data_from_url(url_with_data)
print(df)
