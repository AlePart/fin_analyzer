import yfinance as yf
from datetime import date

class DataRepositoryInterface:
    
    def fetch(self, ticker):
        pass

    def get_data_from_date(self, ticker, date: date):
        pass

    def get_data_from_date_range(self, ticker, start_date : date, end_date: date):
        pass

    def get_data(self, ticker):
        pass



class YahooFinanceRepository(DataRepositoryInterface):
    
    def __init__(self):
        self.data = dict()

    def fetch(self, ticker):
        if ticker not in self.data:
            print(f"Fetching data for {ticker}")
            self.data[ticker] = yf.download(ticker)
    
    def get_data_from_date(self, ticker, date : date):
        if ticker not in self.data:
            return None
        return self.data[ticker].loc[date]
    
    def get_data_from_date_range(self, ticker, start_date: date, end_date : date):
        if ticker not in self.data:
            return None
        return self.data[ticker].loc[start_date:end_date]
    
    def get_data(self, ticker):
        if ticker not in self.data:
            return None
        return self.data[ticker]