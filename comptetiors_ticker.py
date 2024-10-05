import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_competitors(ticker):
    # Want to find competitors for the given stock ticker using yfinance
    url = f"https://finance.yahoo.com/quote/{ticker}/profile?p={ticker}"

    #need to mimic browser request
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    s = BeautifulSoup(response.text, 'html.parser')

    # Utilise 'competitors' section in the URL
    competitors = []
    try:
        # Find all links under 'People Also Watch' section
        related_stocks_section = s.find_all('section')
        for section in related_stocks_section:
            links = section.find_all('a')
            for link in links:
                competitor_ticker = link.text.strip()
                if competitor_ticker and competitor_ticker.isupper():
                    competitors.append(competitor_ticker)
    except Exception as e:
        print(f"An error occurred: {e}")

    return competitors

#Testing
# if __name__ == "__main__":
#     test_ticker = "AAPL"
#     competitors = get_competitors(test_ticker)
#     print(f"Competitors for {test_ticker}: {competitors}")