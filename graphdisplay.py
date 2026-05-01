def run_visualize():
    import yfinance as yf
    import sqlite3
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    conn = sqlite3.connect('stocks.db')
    cursor = conn.cursor()

    cursor.execute("SELECT ticker, date, close FROM stock_prices ORDER BY ticker, date")
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ticker', 'date', 'close'])

    # Calculate metrics
    df['daily_return'] = df.groupby('ticker')['close'].pct_change()
    df['MA_20'] = df.groupby('ticker')['close'].transform(lambda x: x.rolling(20, min_periods=1).mean())
    df['MA_50'] = df.groupby('ticker')['close'].transform(lambda x: x.rolling(50, min_periods=1).mean())
    df['volatility'] = df.groupby('ticker')['daily_return'].transform(lambda x: x.rolling(30).std() * np.sqrt(252))


    # # Filter for one stock
    # mahindra = df[df['ticker'] == 'M&M.NS'].copy()

    # plt.figure(figsize=(12, 6))
    # plt.plot(mahindra['date'], mahindra['close'], label='Close Price', linewidth=1.5)
    # plt.plot(mahindra['date'], mahindra['MA_20'], label='20-day MA', linewidth=1)
    # plt.plot(mahindra['date'], mahindra['MA_50'], label='50-day MA', linewidth=1)
    # plt.title('m&M Stock Price with Moving Averages')
    # plt.xlabel('Date')
    # plt.ylabel('Price (INR)')
    # plt.legend()
    # plt.grid(True, alpha=0.3)
    # plt.show()


    #soring for correct first and last values
    df = df.sort_values(['ticker','date'])

    grouped = df.groupby('ticker')

    first_p = round(grouped['close'].first(),2)
    last_p = round(grouped['close'].last(),2)

    returns = (last_p - first_p)/first_p

    volatility = grouped['daily_return'].std() * np.sqrt(252)

    summary_df = pd.DataFrame({
        'return': returns,
        'volatility': volatility
    }).reset_index()

    x = summary_df['volatility'] * 100
    y = summary_df['return'] * 100

    plt.scatter(x, y, color='blue', marker='o', s=50, alpha=0.7)
    plt.title("Risk vs Return")
    plt.xlabel("Volatility (%)")
    plt.ylabel("Returns (%)")

    for i in range(len(summary_df)):
        plt.text(x.iloc[i], y.iloc[i], summary_df['ticker'].iloc[i])

    
    plt.show()


