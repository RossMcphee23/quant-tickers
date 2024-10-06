import yfinance as yf
import pandas as pd
import requests
from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Cache to store industry information for tickers
industry_cache = {}

# Define fallback industry information for known tickers
fallback_industries = {
    'AAPL': {'industry': 'Consumer Electronics', 'short_name': 'Apple Inc.', 'sector': 'Technology'},
    'AMTM': {'industry': 'Unknown', 'short_name': 'AMTM', 'sector': 'Unknown'},
    'CAT': {'industry': 'Farm & Heavy Construction Machinery', 'short_name': 'Caterpillar Inc.', 'sector': 'Industrials'}
}

def get_sp500_tickers():
    # Scrape the list of S&P 500 companies from Wikipedia
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    sp500_df = pd.read_html(StringIO(response.text))[0]
    tickers = sp500_df['Symbol'].str.replace('.', '-', regex=False).tolist()
    return tickers

def fetch_industry_info(ticker):
    try:
        company = yf.Ticker(ticker)
        info = company.info
        industry = info.get('industry', None)
        sector = info.get('sector', None)
        short_name = info.get('shortName', 'N/A')
        
        # Fallback to hardcoded data if industry is not found
        if not industry and ticker in fallback_industries:
            print(f"Using fallback industry information for {ticker}.")
            industry = fallback_industries[ticker]['industry']
            short_name = fallback_industries[ticker]['short_name']
            sector = fallback_industries[ticker]['sector']
        
        if industry:
            return {
                'ticker': ticker,
                'industry': industry,
                'short_name': short_name,
                'sector': sector
            }
        
        print(f"Industry information not found for {ticker}. Available info: {info.keys()}")
    except Exception as e:
        print(f"An error occurred while fetching data for {ticker}: {e}")
    return None

def fetch_all_industries(tickers):
    # Use multithreading to fetch data for each ticker
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(fetch_industry_info, ticker): ticker for ticker in tickers}
        for future in as_completed(futures):
            result = future.result()
            if result:
                industry_cache[result['ticker']] = {
                    'industry': result['industry'],
                    'short_name': result['short_name'],
                    'sector': result['sector']
                }

def get_industry_from_cache(ticker):
    # Return the cached industry information if available
    return industry_cache.get(ticker, {}).get('industry'), industry_cache.get(ticker, {}).get('sector')

def get_industry_competitors(ticker):
    # Get the industry of the target company from the cache
    target_industry, target_sector = get_industry_from_cache(ticker)
    if not target_industry:
        print(f"Industry information for {ticker} is not available.")
        return []

    print(f"Industry for {ticker}: {target_industry} | Sector: {target_sector}")

    # Find competitors with the same industry or related sector
    competitors = [
        {
            'ticker': potential_ticker,
            'short_name': data['short_name'],
            'industry': data['industry'],
            'sector': data['sector']
        }
        for potential_ticker, data in industry_cache.items()
        if potential_ticker != ticker and (data['industry'] == target_industry or (target_sector and data['sector'] == target_sector))
    ]

    return competitors

# Testing
if __name__ == "__main__":
    # Get S&P 500 tickers
    sp500_tickers = get_sp500_tickers()
    
    # Fetch industry information for all S&P 500 companies
    fetch_all_industries(sp500_tickers)
    
    # Find competitors for the given ticker
    test_ticker = "TSLA"
    competitors = get_industry_competitors(test_ticker)
    
    # Print the results in a nice format
    if competitors:
        competitors_df = pd.DataFrame(competitors)
        print("\nCompetitors for {}: \n".format(test_ticker))
        print(competitors_df.to_string(index=False))
    else:
        print(f"No competitors found for {test_ticker}.")
