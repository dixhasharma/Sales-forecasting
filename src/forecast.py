
import pandas as pd
from sklearn.linear_model import LinearRegression
from pathlib import Path


def forecast_result(selected_category="All Categories"):

    # Step 1: Read existing CSV dataset
    project_path = Path(__file__).resolve().parent.parent
    csv_path = project_path / "dataset" / "sales_data.csv"

    df = pd.read_csv(csv_path)

    # Step 2: Prepare required columns
    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )
    df["Sales"] = pd.to_numeric(
        df["Sales"], errors="coerce"
    )

    df = df.dropna(subset=["Order Date", "Sales"])

    # Step 3: Apply category filter
    if selected_category != "All Categories":
        df = df[df["Category"] == selected_category]

    # Step 4: Calculate monthly sales
    df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()

    df = (
        df.groupby("Month")["Sales"]
        .sum()
        .reset_index()
    )

    df = df.rename(columns={"Sales": "Total_Sales"})

    if len(df) < 12:
        raise Exception(
            "At least 12 months of sales data are required."
        )

    # Step 5: Fill missing months
    df = (
        df.set_index("Month")
        .asfreq("MS", fill_value=0)
        .reset_index()
    )

    # Step 6: Prepare training features
    df["Year"] = df["Month"].dt.year
    df["Month_Number"] = df["Month"].dt.month

    X = pd.get_dummies(
        df[["Year", "Month_Number"]],
        columns=["Month_Number"],
        dtype=int
    )

    y = df["Total_Sales"]

    # Step 7: Train forecasting model
    model = LinearRegression()
    model.fit(X, y)

    # Step 8: Generate next 6 months
    last_month = df["Month"].max()

    future_dates = pd.date_range(
        start=last_month + pd.DateOffset(months=1),
        periods=6,
        freq="MS"
    )

    future_df = pd.DataFrame({
        "Month": future_dates
    })

    future_df["Year"] = future_df["Month"].dt.year
    future_df["Month_Number"] = future_df["Month"].dt.month

    # Step 9: Align future features with training features
    all_dates = pd.concat(
        [
            df[["Year", "Month_Number"]],
            future_df[["Year", "Month_Number"]]
        ],
        ignore_index=True
    )

    all_features = pd.get_dummies(
        all_dates,
        columns=["Month_Number"],
        dtype=int
    )

    future_features = all_features.iloc[len(df):]

    future_features = future_features.reindex(
        columns=X.columns,
        fill_value=0
    )

    # Step 10: Predict future sales
    predictions = model.predict(future_features)

    result = pd.DataFrame({
        "Month": future_dates,
        "Predicted_Sales": predictions.round(2)
    })

    return result
