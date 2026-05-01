import yfinance as yf
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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


cursor.execute("SELECT ticker, date, close FROM stock_prices ORDER BY ticker, date")
data = cursor.fetchall()
df = pd.DataFrame(data, columns=['ticker', 'date', 'close'])

# Calculate metrics
df['daily_return'] = df.groupby('ticker')['close'].pct_change()
df['MA_20'] = df.groupby('ticker')['close'].transform(lambda x: x.rolling(20, min_periods=1).mean())
df['MA_50'] = df.groupby('ticker')['close'].transform(lambda x: x.rolling(50, min_periods=1).mean())
df['volatility'] = df.groupby('ticker')['daily_return'].transform(lambda x: x.rolling(30).std() * np.sqrt(252))


# Filter for one stock
aapl = df[df['ticker'] == 'M&M.NS'].copy()

plt.figure(figsize=(12, 6))
plt.plot(aapl['date'], aapl['close'], label='Close Price', linewidth=1.5)
plt.plot(aapl['date'], aapl['MA_20'], label='20-day MA', linewidth=1)
plt.plot(aapl['date'], aapl['MA_50'], label='50-day MA', linewidth=1)
plt.title('AAPL Stock Price with Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

cursor.execute("""
               SELECT ticker, ROUND(AVG(volume),2) as avg_volume FROM stock_prices
               GROUP BY ticker
               ORDER BY avg_volume DESC
               """)
print(cursor.fetchall())