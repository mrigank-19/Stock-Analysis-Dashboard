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
    
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    df['ticker'] = ticker
    
    stocks_data[ticker] = df
    df = df.dropna()
    df = df.reset_index(drop=True)

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
    volume INTEGER,
    UNIQUE(ticker, date)
);
''')


for ticker, df in stocks_data.items():
    df['date'] = df['date'].astype(str)
    df['volume'] = df['volume'].astype(int)

    records = df[['date', 'open', 'high', 'low', 'close', 'volume', 'ticker']].values.tolist()

    cursor.executemany('''
        INSERT OR IGNORE INTO stock_prices
        (date, open, high, low, close, volume, ticker)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', records)

    
conn.commit()

graphdisplay.run_visualize()