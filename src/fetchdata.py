import yfinance as yf
import pandas as pd

def fetch_sp500_data(start_date="1950-01-01", end_date="2023-12-31"):
    ticker_symbol = "^GSPC"
    print(f"Downloading data for {ticker_symbol} from {start_date} to {end_date}...")
    data = yf.download(ticker_symbol, start=start_date, end=end_date)
    data = data.round(2)
    desired_order = ["Open", "High", "Low", "Close", "Volume"]
    data = data[desired_order]
    return data

def save_data_to_csv(data, filepath="data/sp500_data.csv"):
    data.to_csv(filepath)
    print(f"Data has been saved to: {filepath}")

def main():
    # For daily returns: 2008-2023
    start_date_daily = "2008-01-01"
    end_date_daily = "2023-12-31"
    sp500_data_daily = fetch_sp500_data(start_date_daily, end_date_daily)
    sp500_data_daily['Daily Return'] = sp500_data_daily['Close'].pct_change()
    save_data_to_csv(sp500_data_daily, filepath="data/sp500_daily_returns.csv")

    # For annual means: 1950-2023
    start_date_annual = "1950-01-01"
    end_date_annual = "2023-12-31"
    sp500_data_annual = fetch_sp500_data(start_date_annual, end_date_annual)
    sp500_data_annual['Daily Return'] = sp500_data_annual['Close'].pct_change()
    save_data_to_csv(sp500_data_annual, filepath="data/sp500_annual_data.csv")

if __name__ == "__main__":
    main()
