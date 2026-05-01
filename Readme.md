# 📈 Stock Analysis Dashboard

## 📌 Description
This project analyzes stock data using Python. It fetches data using yfinance, stores it in SQLite, calculates key metrics like returns and volatility, and visualizes them using a scatter plot.

## 🚀 Features
- Data fetching using yfinance
- SQLite database storage
- Financial metrics calculation
- Risk vs Return visualization

## 🛠 Tech Stack
- Python
- pandas, numpy
- matplotlib
- SQLite

## 📂 Project Structure
- main.py → data fetching & storage
- graphdisplay.py → visualization
- stocks.db → database

## ▶️ How to Run
pip install pandas numpy matplotlib yfinance  
python main.py  

## 📊 Output
![alt text](risk_return.png)

## 📌 Insights
- SBIN performed best (high return, low volatility)
- TCS and INFY underperformed
- Risk does not always lead to higher returns

## 🔮 Future Work
- Add Sharpe Ratio
- Build interactive dashboard