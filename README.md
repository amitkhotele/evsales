# ⚡ Electric Vehicle Sales Data Analysis & Forecasting
An interactive data analysis and forecasting project to explore and predict the growth of Electric Vehicle (EV) sales across different states in India.

---

## 🚀 Project Overview
This project provides deep insights into Electric Vehicle (EV) sales trends using data visualization, statistical analysis, and machine learning forecasting.  
The goal is to understand how EV adoption varies by **state**, **vehicle type**, and **time**, and to forecast future EV sales trends in India.

Built with **Python**, **Plotly**, and **Streamlit**, this project delivers a **beautiful, interactive dashboard** where users can:
- Visualize EV sales data by category, year, and location.
- Analyze top-performing states and vehicle types.
- Forecast next year’s EV sales using a time-series model (Prophet).

---

## 🎯 Objectives
- Analyze the growth pattern of EV sales across India.
- Identify the top contributing states and vehicle segments.
- Build an interactive dashboard for visual insights.
- Forecast future sales using machine learning techniques.

---

## 🧰 Tools & Technologies Used

| Category | Tools/Frameworks |
|-----------|------------------|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly, Matplotlib, Seaborn |
| Forecasting | Prophet / ARIMA |
| Web Dashboard | Streamlit |
| Model Persistence | Joblib |

---

## 🧹 Data Preprocessing
- Removed duplicates and standardized date formats.
- Converted EV sales quantities and dates into numeric and datetime formats.
- Aggregated monthly EV sales by **state** and **vehicle type**.
- Handled missing or inconsistent data entries.
- Created new features such as:
  - `Monthly_Sales`
  - `Cumulative_Sales`
  - `Growth_Rate`

---

## 📊 Key Insights
- **Maharashtra**, **Tamil Nadu**, and **Delhi** are top-performing states in EV sales.
- **Two-wheelers** contribute the highest share of total EV sales.
- A strong upward trend is observed in the past few years.
- Seasonality exists — sales tend to increase during mid-year months.
- Forecasting models predict a steady rise in EV adoption over the next year.

---

## 🔮 Machine Learning & Forecasting
The model uses **Facebook Prophet** (or ARIMA fallback) to forecast EV sales for the next 12 months.

### Features Used:
- Date (`ds`)
- Sales Quantity (`y`)
- State
- Vehicle Type

### Metrics:
- RMSE
- MAE
- MAPE

Forecast results are displayed interactively using Plotly charts.

---

## 💻 Streamlit Dashboard
The Streamlit app provides:
- **Interactive Filters:** Select by state and vehicle type.
- **Dynamic Visuals:** Bar charts, line graphs, pie charts, and trend lines.
- **Forecast Section:** Predict next year’s EV sales growth.
- **Footer:** Developer info & contact links.

### Run Locally:
```bash
pip install -r requirements.txt
streamlit run app.py
