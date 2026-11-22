
# Sales Forecasting and Business Intelligence Using Cloud Analytics

## 1. Project Overview
This project analyzes historical sales data and predicts future sales using Machine Learning. It provides interactive dashboards for monitoring sales performance and business insights.

## 2. Objectives
- Analyze historical sales data.
- Identify monthly and category-wise sales trends.
- Predict future sales using Machine Learning.
- Store sales transactions in MySQL.
- Provide interactive dashboards using Grafana.
- Support new sales entry through Streamlit.

## 3. Technologies Used
- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- MySQL
- Streamlit
- Grafana
- Google Cloud Platform (planned cloud integration)

## 4. Machine Learning Model
Algorithm: Linear Regression

Evaluation:
- MAE: 11,395.09
- RMSE: 15,655.22
- MAPE: 17.58%
- Estimated accuracy-style score: 82.42%

## 5. Dashboard Features
- Total Sales
- Total Profit
- Total Transactions
- Monthly Sales Trend
- Category-wise Sales
- Actual vs Predicted Sales

## 6. Real-Time Sales Entry
Users can enter new sales transactions through Streamlit. The application stores the transactions in MySQL, and Grafana refreshes its dashboard periodically to display updated information.

## 7. Project Structure
- dataset/: Historical sales dataset
- notebooks/: Analysis notebooks
- src/: Python source code
- models/: Trained ML model
- dashboard/: Dashboard-related files

## 8. How to Run
1. Start MySQL Server.
2. Open the project folder in VS Code.
3. Run the Streamlit application:

python -m streamlit run src/app.py

4. Open Grafana at http://localhost:3000.

## 9. Conclusion
This project combines Machine Learning, database management, and Business Intelligence to analyze historical sales, generate future sales forecasts, and support business decision-making.
