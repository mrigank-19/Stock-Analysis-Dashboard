-- best performing stock by return

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

-- Avg Volume Per Stock
SELECT ticker, ROUND(AVG(volume) / 10000000.0, 2) AS "avg_vol(cr)" FROM stock_prices
GROUP BY ticker
ORDER BY "avg_vol(cr)" DESC;


-- Dates where stock moves up 2%
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
