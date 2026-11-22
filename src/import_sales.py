
import pandas as pd
from mysql_connection import create_connection

# Load historical sales dataset
df = pd.read_excel("dataset/sales_data.xls")

# Connect to MySQL
connection = create_connection()

if connection:
    cursor = connection.cursor()

    sql = """
    INSERT INTO sales (
        order_id,
        order_date,
        customer_id,
        customer_name,
        category,
        sub_category,
        product_name,
        quantity,
        unit_price,
        sales,
        discount,
        profit,
        entry_source
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    records = []

    for _, row in df.iterrows():
        quantity = int(row["Quantity"])
        sales = float(row["Sales"])

        unit_price = sales / quantity if quantity > 0 else 0

        records.append((
            str(row["Order ID"]),
            pd.to_datetime(row["Order Date"]).date(),
            str(row["Customer ID"]),
            str(row["Customer Name"]),
            str(row["Category"]),
            str(row["Sub-Category"]),
            str(row["Product Name"]),
            quantity,
            unit_price,
            sales,
            float(row["Discount"]),
            float(row["Profit"]),
            "historical"
        ))

    cursor.executemany(sql, records)
    connection.commit()

    print("Historical sales imported successfully!")
    print("Total records imported:", cursor.rowcount)

    cursor.close()
    connection.close()
