import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_competitors(ticker):
    # Want to find competitors for the given stock ticker using yfinance
    url = f"https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}"
    response = requests.get(url)
    s = BeautifulSoup(response.text, 'html.parser')

    