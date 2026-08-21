# generate_dataset.py

import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from faker import Faker


# ============================================================
# PROJECT PATHS
# ============================================================

# Get the folder containing this Python file:
# sales-business-analytics/python/
PYTHON_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one level up to:
# sales-business-analytics/
PROJECT_ROOT = os.path.dirname(PYTHON_DIR)

# Create the correct raw-data path:
# sales-business-analytics/data/raw/
RAW_DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "raw"
)

# Final CSV location:
OUTPUT_FILE = os.path.join(
    RAW_DATA_DIR,
    "sales_data.csv"
)


# ============================================================
# CONFIGURATION
# ============================================================

NUM_RECORDS = 15000

fake = Faker()

# Fixed seeds make the dataset reproducible.
# Running the script again will generate the same dataset.
random.seed(42)
np.random.seed(42)


# ============================================================
# BUSINESS DIMENSIONS
# ============================================================

regions = {
    "West": {
        "states": [
            "California",
            "Washington",
            "Oregon",
            "Nevada",
            "Arizona"
        ],
        "cities": [
            "Los Angeles",
            "San Francisco",
            "San Diego",
            "Seattle",
            "Portland",
            "Las Vegas",
            "Phoenix"
        ],
    },

    "East": {
        "states": [
            "New York",
            "Massachusetts",
            "New Jersey",
            "Pennsylvania",
            "Virginia"
        ],
        "cities": [
            "New York",
            "Boston",
            "Newark",
            "Philadelphia",
            "Richmond"
        ],
    },

    "Central": {
        "states": [
            "Texas",
            "Illinois",
            "Ohio",
            "Michigan",
            "Missouri"
        ],
        "cities": [
            "Houston",
            "Dallas",
            "Chicago",
            "Columbus",
            "Detroit",
            "St. Louis"
        ],
    },

    "South": {
        "states": [
            "Florida",
            "Georgia",
            "North Carolina",
            "Tennessee",
            "Alabama"
        ],
        "cities": [
            "Miami",
            "Atlanta",
            "Charlotte",
            "Nashville",
            "Birmingham"
        ],
    },
}


# ============================================================
# PRODUCT CATALOG
# ============================================================

categories = {

    "Technology": {

        "Computers": [
            ("Laptop", 850),
            ("Desktop PC", 720),
            ("Monitor", 260),
            ("Tablet", 410),
        ],

        "Accessories": [
            ("Wireless Keyboard", 50),
            ("Wireless Mouse", 35),
            ("Headset", 75),
            ("Webcam", 90),
        ],

        "Phones": [
            ("Smartphone", 650),
            ("Premium Smartphone", 1050),
            ("Phone Charger", 30),
        ],
    },

    "Office Supplies": {

        "Paper": [
            ("Copy Paper", 25),
            ("Premium Paper Pack", 35),
        ],

        "Binders": [
            ("Standard Binder", 18),
            ("Premium Binder", 32),
            ("Presentation Binder", 45),
        ],

        "Storage": [
            ("File Box", 22),
            ("Storage Cabinet", 180),
            ("Document Organizer", 40),
        ],
    },

    "Furniture": {

        "Chairs": [
            ("Office Chair", 220),
            ("Ergonomic Chair", 420),
            ("Executive Chair", 550),
        ],

        "Tables": [
            ("Office Desk", 450),
            ("Conference Table", 900),
            ("Workstation", 700),
        ],

        "Storage": [
            ("Bookshelf", 280),
            ("Filing Cabinet", 320),
        ],
    },
}


# ============================================================
# OTHER BUSINESS DIMENSIONS
# ============================================================

segments = [
    "Consumer",
    "Corporate",
    "Home Office"
]

payment_modes = [
    "Credit Card",
    "Debit Card",
    "Bank Transfer",
    "PayPal"
]

shipping_modes = [
    "Standard",
    "Second Class",
    "First Class",
    "Same Day"
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def random_date(start_date, end_date):
    """
    Generate a random date between start_date and end_date.
    """
    days = (end_date - start_date).days

    return start_date + timedelta(
        days=random.randint(0, days)
    )


def choose_region():
    """
    Select a region using weighted probabilities.
    """

    return random.choices(
        list(regions.keys()),
        weights=[30, 25, 25, 20],
        k=1
    )[0]


def choose_product():
    """
    Select category, sub-category, product and base price.
    """

    category = random.choices(
        list(categories.keys()),
        weights=[45, 30, 25],
        k=1
    )[0]

    sub_category = random.choice(
        list(categories[category].keys())
    )

    product_name, base_price = random.choice(
        categories[category][sub_category]
    )

    return (
        category,
        sub_category,
        product_name,
        base_price
    )


# ============================================================
# GENERATE DATA
# ============================================================

records = []

start_date = datetime(
    2024,
    1,
    1
)

end_date = datetime(
    2025,
    12,
    31
)


# Customer cache ensures the same customer ID
# keeps the same customer name.
customer_cache = {}


for i in range(
    1,
    NUM_RECORDS + 1
):

    # --------------------------------------------------------
    # Order information
    # --------------------------------------------------------

    order_id = f"ORD-{100000 + i}"

    order_date = random_date(
        start_date,
        end_date
    )


    # --------------------------------------------------------
    # Customer information
    # --------------------------------------------------------

    customer_id = (
        f"CUST-{random.randint(1000, 2999)}"
    )

    if customer_id not in customer_cache:

        customer_cache[customer_id] = fake.name()

    customer_name = customer_cache[
        customer_id
    ]


    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    region = choose_region()

    state = random.choice(
        regions[region]["states"]
    )

    city = random.choice(
        regions[region]["cities"]
    )


    # --------------------------------------------------------
    # Customer segment
    # --------------------------------------------------------

    segment = random.choices(
        segments,
        weights=[55, 30, 15],
        k=1
    )[0]


    # --------------------------------------------------------
    # Product
    # --------------------------------------------------------

    (
        category,
        sub_category,
        product_name,
        base_price
    ) = choose_product()

    product_id = (
        f"P-{random.randint(1000, 9999)}"
    )


    # --------------------------------------------------------
    # Quantity
    # --------------------------------------------------------

    quantity = random.choices(
        [1, 2, 3, 4, 5, 6, 7, 8],
        weights=[25, 22, 18, 12, 9, 6, 5, 3],
        k=1
    )[0]


    # --------------------------------------------------------
    # Pricing
    # --------------------------------------------------------

    unit_price = round(
        base_price
        * np.random.uniform(
            0.90,
            1.10
        ),
        2
    )


    # --------------------------------------------------------
    # Discount
    # --------------------------------------------------------

    discount = random.choices(
        [
            0,
            0.05,
            0.10,
            0.15,
            0.20
        ],
        weights=[
            20,
            25,
            30,
            18,
            7
        ],
        k=1
    )[0]


    # --------------------------------------------------------
    # Revenue
    # --------------------------------------------------------

    sales = (
        quantity
        * unit_price
        * (1 - discount)
    )


    # --------------------------------------------------------
    # Cost
    # --------------------------------------------------------

    # Cost represents approximately
    # 58%–82% of the selling price.
    cost_percentage = np.random.uniform(
        0.58,
        0.82
    )

    cost = (
        quantity
        * unit_price
        * cost_percentage
    )


    # --------------------------------------------------------
    # Profit
    # --------------------------------------------------------

    profit = sales - cost


    # --------------------------------------------------------
    # Store record
    # --------------------------------------------------------

    records.append(
        {
            "Order_ID": order_id,

            "Order_Date":
                order_date.strftime(
                    "%Y-%m-%d"
                ),

            "Customer_ID":
                customer_id,

            "Customer_Name":
                customer_name,

            "Region":
                region,

            "State":
                state,

            "City":
                city,

            "Segment":
                segment,

            "Category":
                category,

            "Sub_Category":
                sub_category,

            "Product_ID":
                product_id,

            "Product_Name":
                product_name,

            "Quantity":
                quantity,

            "Unit_Price":
                round(
                    unit_price,
                    2
                ),

            "Discount":
                discount,

            "Sales":
                round(
                    sales,
                    2
                ),

            "Cost":
                round(
                    cost,
                    2
                ),

            "Profit":
                round(
                    profit,
                    2
                ),

            "Payment_Mode":
                random.choice(
                    payment_modes
                ),

            "Shipping_Mode":
                random.choice(
                    shipping_modes
                ),
        }
    )


# ============================================================
# CREATE DATAFRAME
# ============================================================

df = pd.DataFrame(
    records
)


# ============================================================
# SORT DATA
# ============================================================

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"]
)

df = (
    df
    .sort_values(
        "Order_Date"
    )
    .reset_index(
        drop=True
    )
)


# Convert date back to YYYY-MM-DD
# for clean CSV storage.
df["Order_Date"] = (
    df["Order_Date"]
    .dt.strftime(
        "%Y-%m-%d"
    )
)


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(
    RAW_DATA_DIR,
    exist_ok=True
)


# ============================================================
# SAVE CSV
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print("=" * 60)

print(
    "SALES DATASET GENERATED SUCCESSFULLY"
)

print("=" * 60)

print(
    f"Rows generated     : {len(df):,}"
)

print(
    f"Columns             : {len(df.columns)}"
)

print(
    f"Output file         : {OUTPUT_FILE}"
)


# ------------------------------------------------------------
# Confirm file exists
# ------------------------------------------------------------

if os.path.exists(OUTPUT_FILE):

    file_size = os.path.getsize(
        OUTPUT_FILE
    )

    print(
        f"File size           : "
        f"{file_size:,} bytes"
    )

else:

    print(
        "ERROR: Output file was not created."
    )


# ------------------------------------------------------------
# Columns
# ------------------------------------------------------------

print("\nColumns:")

print(
    list(df.columns)
)


# ------------------------------------------------------------
# First five rows
# ------------------------------------------------------------

print("\nFirst 5 records:")

print(
    df.head()
)


# ------------------------------------------------------------
# Missing values
# ------------------------------------------------------------

print("\nMissing values:")

print(
    df.isnull().sum()
)


# ------------------------------------------------------------
# Basic statistics
# ------------------------------------------------------------

print("\nBasic statistics:")

print(
    df[
        [
            "Quantity",
            "Unit_Price",
            "Sales",
            "Cost",
            "Profit"
        ]
    ].describe()
)


print("\n" + "=" * 60)

print(
    "DATASET GENERATION COMPLETE"
)

print("=" * 60)