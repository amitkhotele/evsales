# -------------------------------------------------
# EV Sales Dashboard (Streamlit)
# -------------------------------------------------
# Author: Amit Khotele | Internship Project
# -------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("EVsales_cleaned.csv", parse_dates=["Date"])
    except FileNotFoundError:
        df = pd.read_csv("EVsales.csv")
        df["Year"] = df["Year"].astype(int)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

df = load_data()

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="EV Sales India Dashboard", layout="wide")
st.title("⚡ Electric Vehicle Sales in India")

# -----------------------------
# Sidebar Filters (Simplified)
# -----------------------------
st.sidebar.header("🔎 Filters")

# Year filter (range slider)
min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
year_range = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# State filter (dropdown)
state_list = sorted(df["State"].unique())
selected_state = st.sidebar.selectbox("Select State", ["All States"] + state_list)

# Vehicle Type filter (radio)
vehicle_type_list = sorted(df["Vehicle_Type"].unique())
selected_vehicle_type = st.sidebar.radio("Select Vehicle Type", ["All Types"] + vehicle_type_list)

# Apply filter conditions
df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

if selected_state != "All States":
    df_filtered = df_filtered[df_filtered["State"] == selected_state]

if selected_vehicle_type != "All Types":
    df_filtered = df_filtered[df_filtered["Vehicle_Type"] == selected_vehicle_type]
    
# -----------------------------
# Fixed Sidebar Footer (CSS + HTML)
# -----------------------------
st.markdown(
    """
    <style>
    /* Sidebar footer fixed at bottom */
    [data-testid="stSidebar"] {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .sidebar-footer {
        font-size: 13px;
        color: gray;
        text-align: center;
        padding: 10px 5px;
    }
    .sidebar-footer a {
        text-decoration: none;
        color: gray;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <div class="sidebar-footer">
        👨‍💻 <b>Analyzed by <span style="color:orange">Amit Khotele</span></b><br>
        <a href="mailto:amitkhotele2@gmail.com" target="_blank">📧 Email</a> |
        <a href="https://www.linkedin.com/in/amitkhotele" target="_blank">💼 LinkedIn</a> |
        <a href="https://github.com/amitkhotele" target="_blank">🐙 GitHub</a><br>
    </div>
    """,
    unsafe_allow_html=True
)


# KPI Section

st.subheader("📊 Key Metrics")

total_sales = int(df_filtered["EV_Sales_Quantity"].sum())
top_state = df_filtered.groupby("State")["EV_Sales_Quantity"].sum().idxmax()
top_vehicle_type = df_filtered.groupby("Vehicle_Type")["EV_Sales_Quantity"].sum().idxmax()
top_year = df_filtered.groupby("Year")["EV_Sales_Quantity"].sum().idxmax()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total EV Sales", f"{total_sales:,}")
col2.metric("Top State", top_state)
col3.metric("Top Vehicle Type", top_vehicle_type)
col4.metric("Best Year", top_year)

# -----------------------------
# Visualization Section
# -----------------------------

# Row 1: Sales Trend & Area Chart
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Sales Trend Over Years")
    sales_trend = df_filtered.groupby("Year")["EV_Sales_Quantity"].sum().reset_index()
    fig1 = px.line(sales_trend, x="Year", y="EV_Sales_Quantity", markers=True,
                   title="EV Sales Over Years", line_shape="spline")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🌱 Sales Growth (Area)")
    fig2 = px.area(sales_trend, x="Year", y="EV_Sales_Quantity",
                   title="Cumulative EV Sales Growth", color_discrete_sequence=["green"])
    st.plotly_chart(fig2, use_container_width=True)

# Row 2: State-wise Sales & Heatmap
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌍 State-wise EV Sales")
    state_sales = df_filtered.groupby("State")["EV_Sales_Quantity"].sum().sort_values(ascending=False).reset_index()
    fig3 = px.bar(state_sales.head(15), x="EV_Sales_Quantity", y="State", orientation="h",
                  title="Top 15 States by EV Sales", color="EV_Sales_Quantity", color_continuous_scale="viridis")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("🔥 Heatmap: Year vs State")
    heatmap = df_filtered.groupby(["Year","State"])["EV_Sales_Quantity"].sum().reset_index()
    fig4 = px.density_heatmap(heatmap, x="Year", y="State", z="EV_Sales_Quantity",
                              color_continuous_scale="Blues", title="EV Sales Heatmap")
    st.plotly_chart(fig4, use_container_width=True)

# Row 3: Vehicle Category vs Class
col1, col2 = st.columns(2)

with col1:
    st.subheader("🚙 Sales by Vehicle Category")
    vehicle_cat = df_filtered.groupby("Vehicle_Category")["EV_Sales_Quantity"].sum().reset_index()
    fig5 = px.pie(vehicle_cat, names="Vehicle_Category", values="EV_Sales_Quantity",
                  title="EV Sales by Vehicle Category", hole=0.4)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.subheader("🚌 Sales by Vehicle Class")
    vehicle_class = df_filtered.groupby("Vehicle_Class")["EV_Sales_Quantity"].sum().reset_index()
    fig6 = px.treemap(vehicle_class, path=["Vehicle_Class"], values="EV_Sales_Quantity",
                      title="Treemap of Vehicle Class Sales")
    st.plotly_chart(fig6, use_container_width=True)

# Row 4: Distribution Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Boxplot: Sales Distribution by Year")
    fig7 = px.box(df_filtered, x="Year", y="EV_Sales_Quantity", points="all",
                  title="EV Sales Distribution per Year")
    st.plotly_chart(fig7, use_container_width=True)

with col2:
    st.subheader("📊 Monthly Seasonality")
    monthly_sales = df_filtered.groupby("Month_Name")["EV_Sales_Quantity"].sum().reset_index()
    fig8 = px.bar(monthly_sales, x="Month_Name", y="EV_Sales_Quantity",
                  title="Monthly EV Sales Seasonality", color="EV_Sales_Quantity")
    st.plotly_chart(fig8, use_container_width=True)

# -----------------------------
# Forecast Section (Simple & Clear)
# -----------------------------
st.subheader("🔮 EV Sales Forecast (Next 12 Months)")

from prophet import Prophet

# User chooses filters
forecast_state = st.selectbox("🌍 Select State", ["All States"] + sorted(df["State"].unique()))
forecast_vehicle = st.selectbox("🚙 Select Vehicle Type", ["All Types"] + sorted(df["Vehicle_Type"].unique()))

# Filter dataset
df_forecast = df.copy()
if forecast_state != "All States":
    df_forecast = df_forecast[df_forecast["State"] == forecast_state]
if forecast_vehicle != "All Types":
    df_forecast = df_forecast[df_forecast["Vehicle_Type"] == forecast_vehicle]

# Prepare monthly sales
monthly_sales = df_forecast.groupby(pd.Grouper(key="Date", freq="M"))["EV_Sales_Quantity"].sum().reset_index()
monthly_sales.columns = ["ds", "y"]

if len(monthly_sales) > 12:  # at least 1 year of data
    # Train Prophet model
    m = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
    m.fit(monthly_sales)

    # Make future dataframe (next 12 months)
    future = m.make_future_dataframe(periods=12, freq="M")
    forecast = m.predict(future)

    # Plot simple line chart
    fig = px.line(title=f"📈 EV Sales Forecast for {forecast_state if forecast_state!='All States' else 'India'} ({forecast_vehicle})")
    fig.add_scatter(x=monthly_sales["ds"], y=monthly_sales["y"], mode="lines+markers", name="Historical Sales")
    fig.add_scatter(x=forecast["ds"], y=forecast["yhat"], mode="lines", name="Forecast", line=dict(color="orange"))

    st.plotly_chart(fig, use_container_width=True)

    # Show summary
    next_year_total = int(forecast.tail(12)["yhat"].sum())
    st.success(f"✅ Expected EV Sales in next 12 months: **{next_year_total:,} units**")
else:
    st.warning("⚠️ Not enough historical data to forecast for this selection.")


# -----------------------------
# Data Explorer
# -----------------------------
st.subheader("🗂 Explore Data")
st.dataframe(df_filtered.head(200))
