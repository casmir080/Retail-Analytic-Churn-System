import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# -----------------------
# CONFIG
# -----------------------
st.set_page_config(page_title="RIAP Dashboard", layout="wide")

# -----------------------
# DARK UI
# -----------------------
st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
.stMetric {background-color: #1c1f26; padding: 10px; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

st.title("📊 Retail Intelligence Dashboard")

# -----------------------
# LOAD ENV
# -----------------------
load_dotenv()

engine = create_engine(
    f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
    f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)

@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM customer_rfm_features", engine)

df = load_data()

# -----------------------
# SIDEBAR
# -----------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Overview", "Segmentation", "Churn & Prediction", "Trends", "Customers"]
)

# Filters
st.sidebar.subheader("Filters")

risk_filter = st.sidebar.multiselect(
    "Churn Risk",
    df["churn_risk"].unique(),
    default=df["churn_risk"].unique()
)

df = df[df["churn_risk"].isin(risk_filter)]

# Currency toggle
currency = st.sidebar.selectbox("Currency", ["USD ($)", "Naira (₦)"])
symbol = "$" if "USD" in currency else "₦"
rate = 1 if symbol == "$" else 1500

# -----------------------
# OVERVIEW
# -----------------------
if page == "Overview":

    st.header("Executive Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Customers", df["customer_id"].nunique())
    col2.metric("Revenue", f"{symbol}{df['monetary'].sum()*rate:,.0f}")
    col3.metric("Avg Order", f"{symbol}{df['avg_order_value'].mean()*rate:.2f}")
    col4.metric("High Risk", (df["churn_risk"] == "high").sum())

    # Revenue by segment
    st.subheader("Revenue by Segment")

    rev_seg = df.groupby("churn_risk")["monetary"].sum().reset_index()

    fig = px.bar(rev_seg, x="churn_risk", y="monetary", color="churn_risk")
    st.plotly_chart(fig, use_container_width=True)

    # Customer distribution
    st.subheader("Customer Distribution")

    cust_seg = df["churn_risk"].value_counts().reset_index()
    cust_seg.columns = ["churn_risk", "count"]

    fig = px.bar(cust_seg, x="churn_risk", y="count", color="churn_risk")
    st.plotly_chart(fig, use_container_width=True)

    # Scatter
    st.subheader("Customer Value Analysis")

    fig = px.scatter(
        df,
        x="frequency",
        y="monetary",
        color="churn_risk",
        size="avg_order_value",
        hover_data=["customer_id"]
    )
    st.plotly_chart(fig, use_container_width=True)

    # Top 10
    st.subheader("Top 10 Customers")

    top10 = df.sort_values("monetary", ascending=False).head(10)

    fig = px.bar(top10, x="customer_id", y="monetary", color="churn_risk")
    st.plotly_chart(fig, use_container_width=True)

    # Insights
    st.subheader("AI Insights")

    high = df[df["churn_risk"] == "high"].shape[0]
    total = df.shape[0]

    st.warning(f"{high} customers at high risk ({round(high/total*100,2)}%)")

    st.write("""
    Key Insights:
    - High-frequency customers generate most revenue
    - High-risk segment shows low engagement
    - Medium-risk customers are best upsell targets

    Actions:
    - Run retention campaigns for high-risk users
    - Reward loyal customers
    - Upsell medium-risk segment
    """)

# -----------------------
# SEGMENTATION
# -----------------------
elif page == "Segmentation":

    st.header("Customer Segmentation")

    fig = px.scatter(
        df,
        x="recency",
        y="monetary",
        color="churn_risk",
        size="frequency",
        hover_data=["customer_id"]
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# CHURN + ML
# -----------------------
elif page == "Churn & Prediction":

    st.header("Churn Analysis")

    fig = px.pie(df, names="churn_risk")
    st.plotly_chart(fig)

    st.subheader("Predict Churn")

    col1, col2, col3 = st.columns(3)

    recency = col1.slider("Recency", 0, 200, 30)
    frequency = col2.slider("Frequency", 1, 20, 5)
    monetary = col3.slider("Monetary", 10, 1000, 200)

    if st.button("Predict"):

        try:
            res = requests.post(
                "http://127.0.0.1:8000/predict",
                params={
                    "recency": recency,
                    "frequency": frequency,
                    "monetary": monetary
                }
            )

            result = res.json()

            label_map = {
                0: "Low Risk",
                1: "Medium Risk",
                2: "High Risk"
            }

            st.success(
                f"{label_map[result['prediction']]} | Confidence: {result['confidence']}"
            )

        except:
            st.error("Start FastAPI: uvicorn backend.api.main:app --reload")

# -----------------------
# TRENDS
# -----------------------
elif page == "Trends":

    st.header("Revenue Trends")

    trend = pd.read_sql("""
        SELECT DATE(order_date) as date, SUM(total_price) as revenue
        FROM customer_order_features
        GROUP BY date
        ORDER BY date
    """, engine)

    fig = px.line(trend, x="date", y="revenue")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------
# CUSTOMERS
# -----------------------
elif page == "Customers":

    st.header("Top Customers Table")

    top = df.sort_values("monetary", ascending=False).head(20)

    top["monetary"] = top["monetary"] * rate

    st.dataframe(top)

    csv = top.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "top_customers.csv",
        "text/csv"
    )