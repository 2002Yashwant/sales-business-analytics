-- ============================================================
-- ADVANCED SQL BUSINESS ANALYSIS
-- Sales & Business Performance Analytics
-- ============================================================

USE sales_analytics;


-- ============================================================
-- 1. RANK PRODUCTS BY REVENUE
-- ============================================================

WITH product_sales AS (
    SELECT
        Product_ID,
        Product_Name,
        ROUND(SUM(Sales), 2) AS revenue
    FROM sales
    GROUP BY
        Product_ID,
        Product_Name
)

SELECT
    Product_ID,
    Product_Name,
    revenue,
    RANK() OVER (
        ORDER BY revenue DESC
    ) AS revenue_rank
FROM product_sales
ORDER BY revenue_rank;


-- ============================================================
-- 2. TOP 10 PRODUCTS USING RANKING
-- ============================================================

WITH product_sales AS (
    SELECT
        Product_ID,
        Product_Name,
        ROUND(SUM(Sales), 2) AS revenue
    FROM sales
    GROUP BY
        Product_ID,
        Product_Name
),

ranked_products AS (
    SELECT
        Product_ID,
        Product_Name,
        revenue,
        RANK() OVER (
            ORDER BY revenue DESC
        ) AS revenue_rank
    FROM product_sales
)

SELECT
    Product_ID,
    Product_Name,
    revenue,
    revenue_rank
FROM ranked_products
WHERE revenue_rank <= 10
ORDER BY revenue_rank;


-- ============================================================
-- 3. TOP 3 PRODUCTS WITHIN EACH CATEGORY
-- ============================================================

WITH product_sales AS (
    SELECT
        Category,
        Product_ID,
        Product_Name,
        ROUND(SUM(Sales), 2) AS revenue
    FROM sales
    GROUP BY
        Category,
        Product_ID,
        Product_Name
),

ranked_products AS (
    SELECT
        Category,
        Product_ID,
        Product_Name,
        revenue,

        ROW_NUMBER() OVER (
            PARTITION BY Category
            ORDER BY revenue DESC
        ) AS category_rank

    FROM product_sales
)

SELECT
    Category,
    Product_ID,
    Product_Name,
    revenue,
    category_rank
FROM ranked_products
WHERE category_rank <= 3
ORDER BY
    Category,
    category_rank;


-- ============================================================
-- 4. MONTHLY REVENUE GROWTH
-- ============================================================

WITH monthly_sales AS (
    SELECT
        `Year_Month`,
        ROUND(SUM(Sales), 2) AS revenue
    FROM sales
    GROUP BY `Year_Month`
),

monthly_growth AS (
    SELECT
        `Year_Month`,
        revenue,

        LAG(revenue) OVER (
            ORDER BY `Year_Month`
        ) AS previous_month_revenue

    FROM monthly_sales
)

SELECT
    `Year_Month`,
    revenue,
    previous_month_revenue,

    ROUND(
        revenue - previous_month_revenue,
        2
    ) AS revenue_change,

    ROUND(
        (
            revenue - previous_month_revenue
        )
        / previous_month_revenue
        * 100,
        2
    ) AS growth_percentage

FROM monthly_growth
ORDER BY `Year_Month`;


-- ============================================================
-- 5. YEAR-OVER-YEAR REVENUE COMPARISON
-- ============================================================

WITH yearly_sales AS (
    SELECT
        Year,
        ROUND(SUM(Sales), 2) AS revenue
    FROM sales
    GROUP BY Year
),

yearly_comparison AS (
    SELECT
        Year,
        revenue,

        LAG(revenue) OVER (
            ORDER BY Year
        ) AS previous_year_revenue

    FROM yearly_sales
)

SELECT
    Year,
    revenue,
    previous_year_revenue,

    ROUND(
        revenue - previous_year_revenue,
        2
    ) AS revenue_change,

    ROUND(
        (
            revenue - previous_year_revenue
        )
        / previous_year_revenue
        * 100,
        2
    ) AS yoy_growth_percentage

FROM yearly_comparison
ORDER BY Year;