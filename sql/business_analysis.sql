-- ============================================================
-- BASIC BUSINESS ANALYSIS
-- Sales & Business Performance Analytics
-- Database: sales_analytics
-- Table: sales
-- ============================================================

USE sales_analytics;    
SELECT
    COUNT(DISTINCT Order_ID) AS total_orders,
    SUM(Quantity) AS total_quantity,
    ROUND(SUM(Sales), 2) AS total_revenue,
    ROUND(SUM(Profit), 2) AS total_profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100,
        2
    ) AS profit_margin,
    ROUND(
        SUM(Sales) / COUNT(DISTINCT Order_ID),
        2
    ) AS average_order_value
FROM sales;


-- ============================================================
-- 2. SALES BY REGION
-- ============================================================

SELECT
    Region,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100,
        2
    ) AS profit_margin
FROM sales
GROUP BY Region
ORDER BY revenue DESC;


-- ============================================================
-- 3. SALES BY CATEGORY
-- ============================================================

SELECT
    Category,
    SUM(Quantity) AS quantity_sold,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100,
        2
    ) AS profit_margin
FROM sales
GROUP BY Category
ORDER BY revenue DESC;


-- ============================================================
-- 4. SUB-CATEGORY PERFORMANCE
-- ============================================================

SELECT
    Payment_Mode,
    COUNT(*) AS transactions,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100,
        2
    ) AS profit_margin
FROM sales
GROUP BY Payment_Mode
ORDER BY revenue DESC;


-- ============================================================
-- 5. TOP 10 PRODUCTS BY REVENUE
-- ============================================================

SELECT
    Product_ID,
    Product_Name,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    SUM(Quantity) AS quantity_sold
FROM sales
GROUP BY
    Product_ID,
    Product_Name
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 6. TOP 10 PRODUCTS BY PROFIT
-- ============================================================

SELECT
    Product_ID,
    Product_Name,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    SUM(Quantity) AS quantity_sold
FROM sales
GROUP BY
    Product_ID,
    Product_Name
ORDER BY profit DESC
LIMIT 10;


-- ============================================================
-- 7. CUSTOMER SEGMENT PERFORMANCE
-- ============================================================

SELECT
    Segment,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100,
        2
    ) AS profit_margin
FROM sales
GROUP BY Segment
ORDER BY revenue DESC;


-- ============================================================
-- 8. MONTHLY REVENUE TREND
-- ============================================================

SELECT
    `Year_Month`,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit
FROM sales
GROUP BY `Year_Month`
ORDER BY `Year_Month`;


-- ============================================================
-- 9. QUARTERLY PERFORMANCE
-- ============================================================

SELECT
    Year,
    Quarter,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100,
        2
    ) AS profit_margin
FROM sales
GROUP BY
    Year,
    Quarter
ORDER BY
    Year,
    Quarter;


-- ============================================================
-- 10. TOP 10 CUSTOMERS BY REVENUE
-- ============================================================

SELECT
    Customer_ID,
    Customer_Name,
    COUNT(DISTINCT Order_ID) AS orders,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit
FROM sales
GROUP BY
    Customer_ID,
    Customer_Name
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 11. LOSS-MAKING TRANSACTIONS
-- ============================================================

SELECT
    COUNT(*) AS loss_transactions,
    ROUND(SUM(Profit), 2) AS total_loss
FROM sales
WHERE Profit < 0;


-- ============================================================
-- 12. LOSS BY CATEGORY
-- ============================================================

SELECT
    Category,
    COUNT(*) AS loss_transactions,
    ROUND(SUM(Profit), 2) AS total_loss
FROM sales
WHERE Profit < 0
GROUP BY Category
ORDER BY total_loss ASC;


-- ============================================================
-- 13. LOSS BY REGION
-- ============================================================

SELECT
    Region,
    COUNT(*) AS loss_transactions,
    ROUND(SUM(Profit), 2) AS total_loss
FROM sales
WHERE Profit < 0
GROUP BY Region
ORDER BY total_loss ASC;


-- ============================================================
-- 14. HIGHEST PROFIT MARGIN PRODUCTS
-- ============================================================

SELECT
    Product_ID,
    Product_Name,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100,
        2
    ) AS profit_margin
FROM sales
GROUP BY
    Product_ID,
    Product_Name
HAVING SUM(Sales) > 1000
ORDER BY profit_margin DESC
LIMIT 10;


-- ============================================================
-- 15. HIGH REVENUE BUT LOW PROFIT PRODUCTS
-- ============================================================

SELECT
    Product_ID,
    Product_Name,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100,
        2
    ) AS profit_margin
FROM sales
GROUP BY
    Product_ID,
    Product_Name
HAVING
    SUM(Sales) > 5000
    AND
    SUM(Profit) / SUM(Sales) < 0.20
ORDER BY revenue DESC;


-- ============================================================
-- 16. DISCOUNT ANALYSIS
-- ============================================================

SELECT
    Discount,
    COUNT(*) AS transactions,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100,
        2
    ) AS profit_margin
FROM sales
GROUP BY Discount
ORDER BY Discount;


-- ============================================================
-- 17. PAYMENT MODE ANALYSIS
-- ============================================================

SELECT
    Payment_Mode,
    COUNT(*) AS transactions,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100,
        2
    ) AS profit_margin
FROM sales
GROUP BY Payment_Mode
ORDER BY revenue DESC;


-- ============================================================
-- 18. SHIPPING MODE ANALYSIS
-- ============================================================

SELECT
    Shipping_Mode,
    COUNT(*) AS transactions,
    ROUND(SUM(Sales), 2) AS revenue,
    ROUND(SUM(Profit), 2) AS profit,
    ROUND(
        SUM(Profit) / SUM(Sales) * 100,
        2
    ) AS profit_margin
FROM sales
GROUP BY Shipping_Mode
ORDER BY revenue DESC;