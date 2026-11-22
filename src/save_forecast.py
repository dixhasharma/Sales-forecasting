import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

from mysql_connection import  create_connection
from forecast import forecast_result

# Generate the latest six-month forecast
forecast_df = forecast_result()

# Connect to MySQL 
connection =  create_connection()
cursor = connection.cursor()

# Save predictions
for _, row in forecast_df.iterrows():
    cursor.execute(
        """
        INSERT INTO sales_forecast (forecast_month, predicted_sales)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
        predicted_sales = VALUES(predicted_sales),
        created_at = CURRENT_TIMESTAMP
        """,
        (row["Month"].date(), float(row["Predicted_Sales"]))
    )

connection.commit()

cursor.close()
connection.close()

print("Forecast saved successfully in MySQL!")
