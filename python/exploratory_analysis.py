import os
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# File paths
# --------------------------------------------------
# ============================================================
# PROJECT PATHS
# ============================================================

PYTHON_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PROJECT_ROOT = os.path.dirname(
    PYTHON_DIR
)

INPUT_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "cleaned_sales_data.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "screenshots"
)

# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("=" * 70)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 70)

print(f"\nRows: {len(df):,}")
print(f"Columns: {len(df.columns)}")


# --------------------------------------------------
# Create output directory
# --------------------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)


# --------------------------------------------------
# 1. Overall Business Metrics
# --------------------------------------------------

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()
total_orders = df["Order_ID"].nunique()
average_order_value = total_sales / total_orders
profit_margin = (total_profit / total_sales) * 100

print("\n" + "-" * 70)
print("OVERALL BUSINESS METRICS")
print("-" * 70)

print(f"Total Revenue       : ${total_sales:,.2f}")
print(f"Total Profit        : ${total_profit:,.2f}")
print(f"Total Orders        : {total_orders:,}")
print(f"Total Quantity      : {total_quantity:,}")
print(f"Average Order Value : ${average_order_value:,.2f}")
print(f"Profit Margin       : {profit_margin:.2f}%")


# --------------------------------------------------
# 2. Regional Performance
# --------------------------------------------------

regional = (
    df.groupby("Region")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .sort_values("Revenue", ascending=False)
)

print("\n" + "-" * 70)
print("REGIONAL PERFORMANCE")
print("-" * 70)

print(regional)


# --------------------------------------------------
# 3. Category Performance
# --------------------------------------------------

category = (
    df.groupby("Category")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
)

category["Profit_Margin"] = (
    category["Profit"] /
    category["Revenue"] *
    100
).round(2)

print("\n" + "-" * 70)
print("CATEGORY PERFORMANCE")
print("-" * 70)

print(category)


# --------------------------------------------------
# 4. Sub-category Performance
# --------------------------------------------------

subcategory = (
    df.groupby("Sub_Category")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_values("Revenue", ascending=False)
)

print("\n" + "-" * 70)
print("TOP SUB-CATEGORIES")
print("-" * 70)

print(subcategory.head(10))


# --------------------------------------------------
# 5. Top Products
# --------------------------------------------------

top_products = (
    df.groupby(
        ["Product_ID", "Product_Name"]
    )
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
)

print("\n" + "-" * 70)
print("TOP 10 PRODUCTS BY REVENUE")
print("-" * 70)

print(top_products.head(10))


# --------------------------------------------------
# 6. Customer Segment Analysis
# --------------------------------------------------

segment = (
    df.groupby("Segment")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order_ID", "nunique")
    )
    .sort_values("Revenue", ascending=False)
)

print("\n" + "-" * 70)
print("CUSTOMER SEGMENT PERFORMANCE")
print("-" * 70)

print(segment)


# --------------------------------------------------
# 7. Monthly Revenue
# --------------------------------------------------

monthly = (
    df.groupby("Year_Month")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .sort_index()
)

print("\n" + "-" * 70)
print("MONTHLY PERFORMANCE")
print("-" * 70)

print(monthly)


# --------------------------------------------------
# 8. Quarterly Performance
# --------------------------------------------------

quarterly = (
    df.groupby(
        ["Year", "Quarter"]
    )
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
    .reset_index()
)

print("\n" + "-" * 70)
print("QUARTERLY PERFORMANCE")
print("-" * 70)

print(quarterly)


# --------------------------------------------------
# 9. Loss-Making Transactions
# --------------------------------------------------

loss_data = df[df["Profit_Status"] == "Loss"]

print("\n" + "-" * 70)
print("LOSS ANALYSIS")
print("-" * 70)

print(f"Loss-making transactions: {len(loss_data):,}")

loss_by_category = (
    loss_data.groupby("Category")
    .agg(
        Loss_Transactions=("Order_ID", "count"),
        Total_Loss=("Profit", "sum")
    )
    .sort_values("Total_Loss")
)

print("\nLoss by Category:")
print(loss_by_category)


# --------------------------------------------------
# 10. Generate Charts
# --------------------------------------------------

# ---- Revenue by Region ----

plt.figure(figsize=(8, 5))

regional["Revenue"].plot(
    kind="bar"
)

plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "revenue_by_region.png"
    ),
    dpi=150
)

plt.close()


# ---- Revenue by Category ----

plt.figure(figsize=(8, 5))

category["Revenue"].plot(
    kind="bar"
)

plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "revenue_by_category.png"
    ),
    dpi=150
)

plt.close()


# ---- Monthly Revenue ----

plt.figure(figsize=(12, 5))

monthly["Revenue"].plot(
    kind="line"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "monthly_revenue_trend.png"
    ),
    dpi=150
)

plt.close()


# ---- Profit by Category ----

plt.figure(figsize=(8, 5))

category["Profit"].plot(
    kind="bar"
)

plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "profit_by_category.png"
    ),
    dpi=150
)

plt.close()


# --------------------------------------------------
# Completion
# --------------------------------------------------

print("\n" + "=" * 70)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nCharts saved inside:")
print(OUTPUT_DIR)