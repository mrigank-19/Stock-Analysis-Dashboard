-- 1. best performing stock by return

SELECT 
    ticker,
    ROUND(((last_close - first_close) / first_close) * 100, 2) AS return_pct
FROM (
    SELECT 
        ticker,
        FIRST_VALUE(close) OVER (PARTITION BY ticker ORDER BY date ASC)  AS first_close,
        FIRST_VALUE(close) OVER (PARTITION BY ticker ORDER BY date DESC) AS last_close
    FROM stock_prices
)
GROUP BY ticker
ORDER BY return_pct DESC
LIMIT 5;

-- 2. Avg Volume Per Stock
SELECT ticker, ROUND(AVG(volume) / 10000000.0, 2) AS "avg_vol(cr)" FROM stock_prices
GROUP BY ticker
ORDER BY "avg_vol(cr)" DESC;


-- 3. Dates where stock moves up 2%
SELECT *
FROM (
    SELECT 
        ticker,
        date,
        close,
        ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) 
        * 100.0 / 
        LAG(close) OVER (PARTITION BY ticker ORDER BY date),2) AS pct_change
    FROM stock_prices
)
WHERE pct_change > 2;


-- 4. A query finding the most pct change per stock

SELECT ticker, MAX(pct_change)
FROM (
    SELECT 
        ticker,
        date,
        close,
        ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) 
        * 100.0 / 
        LAG(close) OVER (PARTITION BY ticker ORDER BY date),2) AS pct_change
    FROM stock_prices
)
GROUP BY ticker;

-- 5. A query showing which month had the best average returns

SELECT month, ROUND(AVG(pct_change),2) AS "Max Avg Return"
FROM (
    SELECT 
        ticker,
        date,
        close,
        strftime('%m', date) AS month,
        ROUND((close - LAG(close) OVER (PARTITION BY ticker ORDER BY date)) 
        * 100.0 / 
        LAG(close) OVER (PARTITION BY ticker ORDER BY date),2) AS pct_change
    FROM stock_prices
)
GROUP BY month
ORDER BY AVG(pct_change) DESC
LIMIT 1;

-- 6. A query finding stocks that closed above their 52-week average

SELECT ticker,ROUND(week_avg, 2) AS "52 Week Avg", ROUND(last_close, 2) AS "Last Close"
FROM (
    SELECT
        ticker,
        date,
        AVG (close) OVER (PARTITION BY ticker) AS week_avg,
        FIRST_VALUE(close) OVER (PARTITION BY ticker ORDER BY date DESC)  AS last_close
    FROM stock_prices
)
WHERE last_close > week_avg
GROUP BY ticker;

