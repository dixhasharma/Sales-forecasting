import pandas as pd

# Load the monthly sales dataset
df = pd.read_csv("dataset/monthly_sales.csv")

# Display the first 5 records
print("===== MONTHLY SALES DATA =====")
print(df.head())

# Check dataset information
print("\n===== DATASET INFORMATION =====")
print(df.info())

# Check total records
print("\nTotal monthly records:", len(df))



# STEP 11: FEATURE ENGINEERING

# Convert Month column into datetime
df["Month"] = pd.to_datetime(df["Month"])

# Extract year and month number
df["Year"] = df["Month"].dt.year
df["Month_Number"] = df["Month"].dt.month

print("\n===== PREPARED MACHINE LEARNING DATA =====")
print(df.head(10))

# Select input features
# Include monthly seasonal patterns

# /////////////////////////
X = pd.get_dummies(
    df[["Year", "Month_Number"]],                 
    columns=["Month_Number"],
    dtype=int
)

# Select target variable
y = df["Total_Sales"]

print("\nINPUT FEATURES:")
print(X.head())

print("\nTARGET VALUES:")
print(y.head())

# STEP 12: SPLIT DATA INTO TRAINING AND TESTING

# First 36 months for training
X_train = X.iloc[:36]
y_train = y.iloc[:36]

# Last 12 months for testing
X_test = X.iloc[36:]
y_test = y.iloc[36:]

print("\n===== TRAINING DATA =====")
print("Training records:", len(X_train))

print("\n===== TESTING DATA =====")
print("Testing records:", len(X_test))

print("\nTesting months:")
print(df["Month"].iloc[36:])


# STEP 13: TRAIN LINEAR REGRESSION MODEL

from sklearn.linear_model import LinearRegression

# Create the model
model = LinearRegression()

# Train the model
model.fit(X_train, y_train)

print("\n===== MODEL TRAINING COMPLETED =====")

# Predict sales for testing data
y_pred = model.predict(X_test)

print("\n===== ACTUAL VS PREDICTED SALES =====")

comparison = pd.DataFrame({
    "Actual Sales": y_test.values,
    "Predicted Sales": y_pred
})

print(comparison)


# STEP 14: EVALUATE MODEL PERFORMANCE

from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# Calculate MAE
mae = mean_absolute_error(y_test, y_pred)

# Calculate RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

print("\n===== MODEL PERFORMANCE =====")
print("Mean Absolute Error (MAE):", round(mae, 2))
print("Root Mean Squared Error (RMSE):", round(rmse, 2))


# STEP 15: VISUALIZE ACTUAL VS PREDICTED SALES

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.plot(
    df["Month"].iloc[36:],
    y_test.values,
    marker="o",
    label="Actual Sales"
)

plt.plot(
    df["Month"].iloc[36:],
    y_pred,
    marker="o",
    label="Predicted Sales"
)

plt.title("Actual vs Predicted Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()

plt.savefig("actual_vs_predicted.png")

plt.show()

# STEP 16: SAVE TRAINED MODEL

import joblib

joblib.dump(model, "models/sales_forecasting_model.pkl")

print("\n===== MODEL SAVED SUCCESSFULLY =====")


from sklearn.metrics import mean_absolute_percentage_error

mape = mean_absolute_percentage_error(y_test, y_pred) * 100

accuracy = 100 - mape

print("MAPE:", round(mape, 2), "%")
print("Estimated Accuracy:", round(accuracy, 2), "%")

from sklearn.metrics import mean_absolute_error

# Baseline: predict every month using the average training sales
baseline_predictions = [y_train.mean()] * len(y_test)

# Calculate baseline error
baseline_mae = mean_absolute_error(y_test, baseline_predictions)

# Compare both models
print("\n===== MODEL COMPARISON =====")
print("Baseline MAE:", round(baseline_mae, 2))
print("ML Model MAE:", round(mean_absolute_error(y_test, y_pred), 2))

if mean_absolute_error(y_test, y_pred) < baseline_mae:
    print("Result: Our ML model performs better than the baseline.")
else:
    print("Result: Our ML model does not outperform the baseline yet.")