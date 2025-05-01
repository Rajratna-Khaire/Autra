# your_app/utils.py

import random

def fetch_stock_data(symbol):
    """
    Simulate fetching live stock data for a symbol (e.g., "RELIANCE").
    In a real case, you'd use an API like Zerodha Kite or Yahoo Finance to get real stock data.
    """
    print(f"Fetching data for {symbol}...")
    
    # Simulate fetching stock price
    price = random.uniform(2400, 2700)  # Random value between 2400 and 2700
    return {'symbol': symbol, 'price': price}

def place_order(symbol, action, quantity):
    """
    Simulate placing a buy/sell order.
    In a real case, you'd use a broker API to place an actual order.
    """
    print(f"Placing {action} order for {quantity} share(s) of {symbol}")
