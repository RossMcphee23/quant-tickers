# financial_info.py

import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from comptetiors_ticker import get_sp500_tickers, fetch_all_industries, get_industry_competitors  # Import necessary functions

class CompetitorsFinancialFetcher:
    def __init__(self, ticker):
        self.ticker = ticker
        self.competitors = []

    def find_competitors(self):
        # Use the imported function to find competitors for the ticker
        self.competitors = get_industry_competitors(self.ticker)
        return self.competitors

    def fetch_financial_info(self, ticker):
        try:
            company = yf.Ticker(ticker)
            info = company.info

            # Extract financial information
            financial_data = {
                'ticker': ticker,
                'short_name': info.get('shortName', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'revenue': info.get('totalRevenue', 'N/A'),
                'profit_margin': info.get('profitMargins', 'N/A'),
                'return_on_assets': info.get('returnOnAssets', 'N/A'),
                'return_on_equity': info.get('returnOnEquity', 'N/A'),
                'debt_to_equity': info.get('debtToEquity', 'N/A'),
                'current_ratio': info.get('currentRatio', 'N/A'),
                'quick_ratio': info.get('quickRatio', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A')
            }
            return financial_data
        except Exception as e:
            print(f"An error occurred while fetching financial data for {ticker}: {e}")
            return None

    def fetch_competitors_financials(self):
        if not self.competitors:
            print(f"No competitors found for {self.ticker}.")
            return []

        financial_info_list = []

        # Use multithreading to speed up fetching data
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = {executor.submit(self.fetch_financial_info, comp['ticker']): comp['ticker'] for comp in self.competitors}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    financial_info_list.append(result)

        return financial_info_list

# Testing the new class
if __name__ == "__main__":
    # Get S&P 500 tickers using the imported function
    sp500_tickers = get_sp500_tickers()
    
    # Fetch industry information for all S&P 500 companies using the imported function
    fetch_all_industries(sp500_tickers)
    
    # Initialize the CompetitorsFinancialFetcher class for a specific ticker
    financial_fetcher = CompetitorsFinancialFetcher("TSLA")
    
    # Find competitors
    competitors = financial_fetcher.find_competitors()
    
    # Fetch financial information for the competitors
    if competitors:
        competitors_financials = financial_fetcher.fetch_competitors_financials()
        financials_df = pd.DataFrame(competitors_financials)
        
        # Display the DataFrame
        print("\nFinancial information for competitors of {}:\n".format(financial_fetcher.ticker))
        print(financials_df.to_string(index=False))
        
        # Optionally, save to a CSV file
        financials_df.to_csv(f"{financial_fetcher.ticker}_competitors_financials.csv", index=False)
        print(f"\nFinancial data saved to {financial_fetcher.ticker}_competitors_financials.csv")
    else:
        print(f"No competitors found for {financial_fetcher.ticker}.")
