
import streamlit as st
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components

# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Sales Forecasting System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM PROFESSIONAL DESIGN
# =====================================================
st.markdown("""
<style>
.stApp {
    background: #F5F6FC;
    color: #20213A;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1450px;
}

section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid #E8E8F2;
}

section[data-testid="stSidebar"] h2 {
    color: #4338CA;
}

.hero {
    background: linear-gradient(120deg, #312E81, #5B42C7, #805AD5);
    padding: 30px 34px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(79, 70, 229, 0.16);
}

.hero h1 {
    color: white !important;
    font-size: 30px !important;
    font-weight: 750;
    margin: 0;
}

.hero p {
    color: #E0E7FF !important;
    font-size: 15px;
    margin-top: 9px;
}

h2, h3 {
    color: #27235B !important;
    font-weight: 700 !important;
}

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E8E7F5;
    border-left: 4px solid #6D5AE6;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 3px 12px rgba(30, 30, 80, 0.04);
}

div[data-testid="stMetricLabel"] {
    color: #77758D !important;
    font-size: 14px;
}

div[data-testid="stMetricValue"] {
    color: #302B65 !important;
    font-weight: 750;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border: 1px solid #E9E7F4;
    border-radius: 15px;
    padding: 12px;
}

button[data-baseweb="tab"] {
    font-weight: 650;
    color: #625F7D;
    padding: 12px 18px;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #5B42C7;
}

.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(110deg, #5145CD, #7654D8);
    color: white;
    border: none;
    border-radius: 9px;
    padding: 10px 20px;
    font-weight: 650;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: #4035A8;
    color: white;
    border: none;
}

div[data-baseweb="input"] input,
div[data-baseweb="select"] {
    border-radius: 8px;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #E9E7F4;
    border-radius: 10px;
}

.stCaption {
    color: #85839A;
}

.footer {
    text-align: center;
    color: #9290A6;
    font-size: 12px;
    padding-top: 25px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# HERO HEADER
# =====================================================
st.markdown("""
<div class="hero">
    <h1>📊 Sales Forecasting & Business Intelligence</h1>
    <p>
        Monitor business performance, analyze sales trends,
        manage transactions and forecast future sales.
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# LOAD EXISTING CSV DATA
# =====================================================
@st.cache_data
def load_sales_data():

    project_path = Path(__file__).resolve().parent.parent
    csv_path = project_path / "dataset" / "sales_data.csv"

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {csv_path}"
        )

    df = pd.read_csv(csv_path)

    required_columns = [
        "Order Date",
        "Category",
        "Sales",
        "Quantity",
        "Customer Name",
        "Product Name"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns in CSV: {missing_columns}"
        )

    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )

    df["Sales"] = pd.to_numeric(
        df["Sales"], errors="coerce"
    )

    df["Quantity"] = pd.to_numeric(
        df["Quantity"], errors="coerce"
    )

    df = df.dropna(
        subset=["Order Date", "Sales", "Quantity"]
    )

    if "Row ID" in df.columns:
        df["sale_id"] = df["Row ID"]
    else:
        df["sale_id"] = range(1, len(df) + 1)

    df["entry_source"] = "Dataset"

    return df


try:
    if "sales_data" not in st.session_state:
        st.session_state.sales_data = load_sales_data()

    sales_data = st.session_state.sales_data.copy()

except Exception as e:
    st.error(f"Unable to load sales dataset: {e}")
    st.stop()


# =====================================================
# SIDEBAR FILTERS
# =====================================================
st.sidebar.markdown("## 🔎 Dashboard Filters")
st.sidebar.caption("Customize the sales data displayed below.")

selected_category = st.sidebar.selectbox(
    "Select Category",
    [
        "All Categories",
        "Furniture",
        "Office Supplies",
        "Technology"
    ]
)

min_date = sales_data["Order Date"].min().date()
max_date = sales_data["Order Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

valid_range = (
    isinstance(selected_dates, (tuple, list))
    and len(selected_dates) == 2
    and selected_dates[0] <= selected_dates[1]
)

if not isinstance(selected_dates, (tuple, list)) or len(selected_dates) != 2:
    st.sidebar.info("Select both start and end dates.")
elif not valid_range:
    st.sidebar.error("Start date must be before end date.")

st.sidebar.divider()

st.sidebar.markdown("### 📌 Project Information")
st.sidebar.caption("Sales Forecasting System")
st.sidebar.caption(
    "Python • Pandas • Streamlit • Machine Learning • Grafana"
)


# =====================================================
# TABS
# =====================================================
tab_dashboard, tab_add, tab_forecast, tab_bi = st.tabs([
    "📈  Dashboard",
    "➕  Add Sale",
    "🔮  Forecast",
    "📊  BI Dashboard"
])


# =====================================================
# PREPARE FILTERED DATA
# =====================================================
def get_filtered_data():

    df = sales_data.copy()

    if valid_range:
        start_date, end_date = selected_dates

        df = df[
            (df["Order Date"].dt.date >= start_date)
            & (df["Order Date"].dt.date <= end_date)
        ]

    if selected_category != "All Categories":
        df = df[
            df["Category"] == selected_category
        ]

    return df


# =====================================================
# TAB 1: DASHBOARD
# =====================================================
with tab_dashboard:

    st.subheader("Business Performance Overview")
    st.caption(
        "A summary of your sales performance and business activity."
    )

    if not valid_range:
        st.info("Please select a valid date range from the sidebar.")

    else:

        filtered_data = get_filtered_data()

        # ---------------------------------------------
        # KPI SUMMARY
        # ---------------------------------------------
        total_sales = float(filtered_data["Sales"].sum())
        transactions = len(filtered_data)
        units = int(filtered_data["Quantity"].sum())

        avg_order = (
            total_sales / transactions
            if transactions > 0 else 0
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "💰 Total Sales",
            f"${total_sales:,.2f}"
        )

        c2.metric(
            "🧾 Transactions",
            f"{transactions:,}"
        )

        c3.metric(
            "📦 Units Sold",
            f"{units:,}"
        )

        c4.metric(
            "🛒 Average Order Value",
            f"${avg_order:,.2f}"
        )

        st.write("")

        # ---------------------------------------------
        # CHARTS
        # ---------------------------------------------
        left, right = st.columns(2)

        with left:

            with st.container(border=True):

                st.subheader("📈 Monthly Sales Trend")

                monthly = (
                    filtered_data
                    .assign(
                        Month=filtered_data["Order Date"].dt.to_period("M").dt.to_timestamp()
                    )
                    .groupby("Month")["Sales"]
                    .sum()
                    .reset_index()
                    .rename(columns={"Sales": "Total_Sales"})
                    .sort_values("Month")
                )

                if not monthly.empty:

                    st.line_chart(
                        monthly,
                        x="Month",
                        y="Total_Sales",
                        color="#7C3AED"
                    )

                else:
                    st.info("No sales data found for these filters.")

        with right:

            with st.container(border=True):

                st.markdown("### 📦 Category-wise Sales")
                st.caption("Compare sales across product categories.")

                by_category = (
                    filtered_data
                    .groupby("Category")["Sales"]
                    .sum()
                    .reset_index()
                    .rename(columns={"Sales": "Total_Sales"})
                    .sort_values(
                        "Total_Sales",
                        ascending=False
                    )
                )

                if not by_category.empty:

                    st.bar_chart(
                        by_category,
                        x="Category",
                        y="Total_Sales",
                        color="#5145CD",
                        use_container_width=True
                    )

                else:
                    st.info("No category sales available.")

        st.write("")

        # ---------------------------------------------
        # RECENT SALES
        # ---------------------------------------------
        with st.container(border=True):

            st.markdown("### 📋 Recent Sales Transactions")
            st.caption("Latest 10 sales records from your dataset.")

            recent = (
                filtered_data
                .sort_values("Order Date", ascending=False)
                .head(10)
                .copy()
            )

            recent = recent.rename(columns={
                "sale_id": "sale_id",
                "Order Date": "order_date",
                "Customer Name": "customer_name",
                "Product Name": "product_name",
                "Category": "category",
                "Quantity": "quantity",
                "Sales": "sales",
                "entry_source": "entry_source"
            })

            recent = recent[
                [
                    "sale_id",
                    "order_date",
                    "customer_name",
                    "product_name",
                    "category",
                    "quantity",
                    "sales",
                    "entry_source"
                ]
            ]

            st.dataframe(
                recent,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "sale_id": "ID",
                    "order_date": "Order Date",
                    "customer_name": "Customer",
                    "product_name": "Product",
                    "category": "Category",
                    "quantity": "Quantity",
                    "sales": st.column_config.NumberColumn(
                        "Sales",
                        format="$%.2f"
                    ),
                    "entry_source": "Entry Source"
                }
            )


# =====================================================
# TAB 2: ADD NEW SALE
# =====================================================
with tab_add:

    st.subheader("➕ Add a New Sale")
    st.caption(
        "Enter transaction details for a temporary demo entry."
    )

    st.info(
        "Online demo mode: new sales are kept in the current "
        "session only and are not permanently saved."
    )

    with st.container(border=True):

        with st.form("sales_entry_form", clear_on_submit=True):

            st.markdown("### Customer & Product Details")

            col1, col2 = st.columns(2)

            with col1:

                customer_name = st.text_input(
                    "Customer Name",
                    placeholder="Enter customer name"
                )

                category = st.selectbox(
                    "Product Category",
                    [
                        "Furniture",
                        "Office Supplies",
                        "Technology"
                    ]
                )

                quantity = st.number_input(
                    "Quantity",
                    min_value=1,
                    step=1
                )

            with col2:

                product_name = st.text_input(
                    "Product Name",
                    placeholder="Enter product name"
                )

                order_date = st.date_input(
                    "Order Date",
                    value=pd.Timestamp.today().date()
                )

                unit_price = st.number_input(
                    "Unit Price ($)",
                    min_value=0.0,
                    step=100.0
                )

            st.write("")

            submitted = st.form_submit_button(
                "💾 Save Sale",
                use_container_width=True
            )

    if submitted:

        if not customer_name.strip() or not product_name.strip():

            st.error(
                "Please enter both customer name and product name."
            )

        elif unit_price <= 0:

            st.error("Unit price must be greater than zero.")

        else:

            total_sales = int(quantity) * float(unit_price)

            new_sale = {
                "Order Date": pd.Timestamp(order_date),
                "Customer Name": customer_name.strip(),
                "Product Name": product_name.strip(),
                "Category": category,
                "Quantity": int(quantity),
                "Sales": total_sales,
                "sale_id": int(sales_data["sale_id"].max()) + 1,
                "entry_source": "Manual"
            }

            st.session_state.sales_data = pd.concat(
                [
                    st.session_state.sales_data,
                    pd.DataFrame([new_sale])
                ],
                ignore_index=True
            )

            st.success(
                "Sale added to the current session successfully!"
            )

            a, b, c = st.columns(3)

            a.metric("Customer", customer_name.strip())
            b.metric("Product", product_name.strip())
            c.metric("Total Sales", f"${total_sales:,.2f}")


# =====================================================
# TAB 3: SALES FORECAST
# =====================================================
with tab_forecast:

    st.subheader("🔮 Future Sales Forecast")
    st.caption(
        "Machine learning-based prediction for the next six months."
    )

    try:

        from forecast import forecast_result

        forecast_df = forecast_result(selected_category)

        if forecast_df is not None and not forecast_df.empty:

            forecast_df = forecast_df.copy()

            forecast_df["Month"] = pd.to_datetime(
                forecast_df["Month"]
            ).dt.strftime("%b %Y")

            forecast_df["Predicted_Sales"] = (
                forecast_df["Predicted_Sales"].astype(float)
            )

            st.success(
                "Six-month sales forecast generated successfully."
            )

            total_forecast = forecast_df["Predicted_Sales"].sum()
            average_forecast = forecast_df["Predicted_Sales"].mean()

            f1, f2 = st.columns(2)

            f1.metric(
                "📊 Total Forecasted Sales",
                f"${total_forecast:,.2f}"
            )

            f2.metric(
                "📅 Average Monthly Forecast",
                f"${average_forecast:,.2f}"
            )

            st.write("")

            chart_col, table_col = st.columns([2, 1])

            with chart_col:

                with st.container(border=True):

                    st.markdown("### 📈 Predicted Sales Trend")

                    st.line_chart(
                        forecast_df,
                        x="Month",
                        y="Predicted_Sales",
                        color="#E9A23B",
                        use_container_width=True
                    )

            with table_col:

                with st.container(border=True):

                    st.markdown("### 📋 Forecast Details")

                    st.dataframe(
                        forecast_df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Month": "Month",
                            "Predicted_Sales": st.column_config.NumberColumn(
                                "Predicted Sales",
                                format="$%.2f"
                            )
                        }
                    )

        else:

            st.warning("No forecast data is available.")

    except Exception as e:

        st.error(f"Error loading forecast: {e}")


# =====================================================
# TAB 4: GRAFANA BI DASHBOARD
# =====================================================
with tab_bi:

    st.subheader("📊 Business Intelligence Dashboard")

    st.caption(
        "Interactive Grafana dashboard displaying business analytics."
    )

    with st.container(border=True):

        st.info(
            "Grafana is running on your local computer. "
            "It will be available in your local project, but "
            "cannot be accessed through this online deployment."
        )


# =====================================================
# FOOTER
# =====================================================
st.markdown("""
<div class="footer">
    Sales Forecasting & Business Intelligence Project
    <br>
    Developed using Python | Pandas | Streamlit | Machine Learning | Grafana
</div>
""", unsafe_allow_html=True)
