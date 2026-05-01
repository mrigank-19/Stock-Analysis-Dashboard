import yfinance as yf
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import graphdisplay


G_stocks = ["RELIANCE.NS", "INFY.NS", "TCS.NS", "M&M.NS", "SBIN.NS"]
stocks_data = {}
for i in G_stocks:
    d = yf.download(i, period="1y")
    stocks_data[i] = d


for ticker, df in stocks_data.items():
    df = df.reset_index()
    
    # Rename columns explicitly (simplest fix)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    df['ticker'] = ticker
    
    df = df.dropna()
    stocks_data[ticker] = df

conn = sqlite3.connect('stocks.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT,
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER
)
''')

for ticker, df in stocks_data.items():
    df.to_sql('stock_prices', conn, if_exists='append', index=False)

    
conn.commit()

graphdisplay.run_visualize()