
import pandas as pd

# Load the Excel sales dataset
file_path = "dataset/sales_data.xls"

df = pd.read_excel(file_path)

# Display the first 5 rows
print("\nFIRST 5 ROWS:")
print(df.head())

# Display dataset information
print("\nDATASET INFORMATION:")
print(df.info())

# Display number of rows and columns
print("\nDATASET SIZE:")
print(df.shape)

# Display column names
print("\nCOLUMN NAMES:")
print(df.columns.tolist())



# Check missing values
print("\nMISSING VALUES:")
print(df.isnull().sum())

# Check duplicate records
print("\nDUPLICATE RECORDS:")
print(df.duplicated().sum())

# Get basic sales statistics
print("\nSALES SUMMARY:")
print(df["Sales"].describe())


# Overall Business Performance

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_quantity = df["Quantity"].sum()

print("\n===== BUSINESS PERFORMANCE =====")

print("Total Sales:", round(total_sales, 2))
print("Total Profit:", round(total_profit, 2))
print("Total Quantity Sold:", total_quantity)



# Sales by Product Category

category_sales = df.groupby("Category")["Sales"].sum()

print("\n===== SALES BY CATEGORY =====")
print(category_sales)

# Sort categories from highest to lowest sales
print("\n===== TOP PERFORMING CATEGORY =====")
print(category_sales.sort_values(ascending=False))



import matplotlib.pyplot as plt

# Calculate sales by category
category_sales = df.groupby("Category")["Sales"].sum()

# Create a bar chart
plt.figure(figsize=(8, 5))

category_sales.plot(kind="bar")

plt.title("Total Sales by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)

plt.tight_layout()

# Save the graph
plt.savefig("sales_by_category.png")

plt.show()
plt.close()


# # Monthly Sales Analysis

# # Group sales by month
# monthly_sales = df.groupby(
#     df["Order Date"].dt.to_period("M")
# )["Sales"].sum()

# print("\n===== MONTHLY SALES =====")
# print(monthly_sales)

# # Find highest and lowest sales months
# print("\nHighest Sales Month:")
# print(monthly_sales.idxmax(), "=", round(monthly_sales.max(), 2))

# print("\nLowest Sales Month:")
# print(monthly_sales.idxmin(), "=", round(monthly_sales.min(), 2))

print("\nMONTHLY ANALYSIS CODE STARTED!")
# STEP 8: MONTHLY SALES ANALYSIS

monthly_sales = df.groupby(
    df["Order Date"].dt.to_period("M")
)["Sales"].sum()

print("\n===== MONTHLY SALES =====")
print(monthly_sales)

print("\nHIGHEST SALES MONTH:")
print(monthly_sales.idxmax())
print("Sales:", round(monthly_sales.max(), 2))

print("\nLOWEST SALES MONTH:")
print(monthly_sales.idxmin())
print("Sales:", round(monthly_sales.min(), 2))

# Create monthly sales graph
plt.figure(figsize=(12, 5))

monthly_sales.index = monthly_sales.index.astype(str)
monthly_sales.plot(kind="line", marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.savefig("monthly_sales_trend.png")

print("\nMonthly graph saved successfully!")
plt.show() 



# STEP 9: PREPARE DATA FOR MACHINE LEARNING

# Convert monthly sales into a DataFrame
monthly_data = monthly_sales.reset_index()

# Rename columns
monthly_data.columns = ["Month", "Total_Sales"]

# Save the prepared dataset
monthly_data.to_csv(
    "dataset/monthly_sales.csv",
    index=False
)

print("\n===== PREPARED DATASET =====")
print(monthly_data.head())

print("\nMonthly dataset saved successfully!")
print("Total monthly records:", len(monthly_data))


# CHECK COUNTRY AND CURRENCY INFORMATION

print("\n===== COUNTRY INFORMATION =====")
print(df["Country/Region"].value_counts())

print("\n===== SALES VALUES =====")
print(df["Sales"].head(10))