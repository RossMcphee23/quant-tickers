import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_competitors(ticker):
    # Want to find competitors for the given stock ticker using yfinance
    url = f"https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}"
    response = requests.get(url)
    s = BeautifulSoup(response.text, 'html.parser')

    # Utilise 'competitors' section in the URL
    competitors = []
    try:
        competitors_section = s.find_all('section', {'data-test': 'quote-header'})[0]
        competitors_link = competitors_section.find_all('a')
        for link in competitors_link:
            competitor_ticker = link.text.strip()
            if competitor_ticker and competitor_ticker.isupper():
                competitors.append(competitor_ticker)
    except IndexError:                         #No competitor
        print(f"Couldn't find competitors for {ticker}")

    return competitors
    