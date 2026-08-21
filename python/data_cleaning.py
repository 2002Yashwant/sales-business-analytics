# data_cleaning.py

import os
import pandas as pd


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
    "raw",
    "sales_data.csv"
)

OUTPUT_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "cleaned_sales_data.csv"
)


# ============================================================
# START
# ============================================================

print("=" * 60)
print("STARTING DATA CLEANING")
print("=" * 60)

print(f"\nInput file:")
print(INPUT_FILE)

print(f"\nOutput file:")
print(OUTPUT_FILE)


# ============================================================
# VERIFY INPUT FILE
# ============================================================

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(
        f"Input file not found:\n{INPUT_FILE}"
    )

input_size = os.path.getsize(INPUT_FILE)

print(
    f"\nInput file size: {input_size:,} bytes"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(
    INPUT_FILE
)

print(
    f"\nOriginal rows: {len(df):,}"
)

print(
    f"Original columns: {len(df.columns)}"
)


# ============================================================
# MISSING VALUES
# ============================================================

print("\nMissing values before cleaning:")

print(
    df.isnull().sum()
)


# ============================================================
# DUPLICATES
# ============================================================

duplicate_count = df.duplicated().sum()

print(
    f"\nDuplicate rows: {duplicate_count}"
)


# ============================================================
# REMOVE DUPLICATES
# ============================================================

df = df.drop_duplicates().copy()


# ============================================================
# DATA TYPE CONVERSION
# ============================================================

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

numeric_columns = [
    "Quantity",
    "Unit_Price",
    "Discount",
    "Sales",
    "Cost",
    "Profit"
]

for column in numeric_columns:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# ============================================================
# REMOVE INVALID RECORDS
# ============================================================

essential_columns = [
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Product_ID",
    "Sales"
]

df = df.dropna(
    subset=essential_columns
).copy()


# ============================================================
# CREATE ANALYTICAL COLUMNS
# ============================================================

# Profit margin
df["Profit_Margin"] = (
    df["Profit"]
    / df["Sales"].replace(0, pd.NA)
) * 100

df["Profit_Margin"] = (
    df["Profit_Margin"]
    .round(2)
)


# Year
df["Year"] = (
    df["Order_Date"]
    .dt.year
)


# Month number
df["Month"] = (
    df["Order_Date"]
    .dt.month
)


# Month name
df["Month_Name"] = (
    df["Order_Date"]
    .dt.strftime("%B")
)


# Quarter
df["Quarter"] = (
    "Q"
    + df["Order_Date"]
    .dt.quarter
    .astype(str)
)


# Year-Month
df["Year_Month"] = (
    df["Order_Date"]
    .dt.to_period("M")
    .astype(str)
)


# ============================================================
# PROFIT STATUS
# ============================================================

df["Profit_Status"] = df["Profit"].apply(
    lambda value:
        "Loss"
        if value < 0
        else "Profit"
)


# ============================================================
# AVERAGE ORDER VALUE
# ============================================================

order_totals = (
    df.groupby("Order_ID")["Sales"]
    .sum()
)

df["Average_Order_Value"] = (
    df["Order_ID"]
    .map(order_totals)
    .round(2)
)


# ============================================================
# REORDER COLUMNS
# ============================================================

column_order = [
    "Order_ID",
    "Order_Date",
    "Year",
    "Month",
    "Month_Name",
    "Quarter",
    "Year_Month",
    "Customer_ID",
    "Customer_Name",
    "Region",
    "State",
    "City",
    "Segment",
    "Category",
    "Sub_Category",
    "Product_ID",
    "Product_Name",
    "Quantity",
    "Unit_Price",
    "Discount",
    "Sales",
    "Cost",
    "Profit",
    "Profit_Margin",
    "Profit_Status",
    "Average_Order_Value",
    "Payment_Mode",
    "Shipping_Mode"
]

df = df[column_order]


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# SAVE CLEANED DATA
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("DATA CLEANING COMPLETED")
print("=" * 60)

print(
    f"\nFinal rows: {len(df):,}"
)

print(
    f"Final columns: {len(df.columns)}"
)

print("\nFinal missing values:")

print(
    df.isnull().sum()
)

print("\nProfit status:")

print(
    df["Profit_Status"]
    .value_counts()
)

print("\nSales summary:")

print(
    df["Sales"].describe()
)

print("\nProfit summary:")

print(
    df["Profit"].describe()
)


# ============================================================
# VERIFY OUTPUT FILE
# ============================================================

if os.path.exists(OUTPUT_FILE):

    output_size = os.path.getsize(
        OUTPUT_FILE
    )

    print(
        f"\nCleaned file size:"
        f" {output_size:,} bytes"
    )

    print(
        "\nCleaned file created at:"
    )

    print(
        OUTPUT_FILE
    )

else:

    raise FileNotFoundError(
        "Cleaned CSV was not created."
    )


print("\n" + "=" * 60)
print("CLEANING PIPELINE COMPLETE")
print("=" * 60)