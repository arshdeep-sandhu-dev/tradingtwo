import yfinance as yf
import sys
import json

def get_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo") # Gets last ~22 trading days
    if hist.empty:
         print(json.dumps({"error": "No data found"}))
         return
         
    # Keep the last 20 days
    hist = hist.tail(20)
    
    data = {
         "ticker": ticker,
         "20_day_high": round(float(hist['High'].max()), 2),
         "20_day_sma": round(float(hist['Close'].mean()), 2),
         "latest_close": round(float(hist['Close'].iloc[-1]), 2)
    }
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    if len(sys.argv) > 1:
         get_data(sys.argv[1].upper())
    else:
         print('{"error": "Please provide a ticker symbol."}')