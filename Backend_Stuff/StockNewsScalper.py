import yfinance as yf

def GathererData(ticker):
    return yf.Ticker(ticker)

if __name__ == "__main__":
    data = GathererData('MSFT')
    print(data.news)