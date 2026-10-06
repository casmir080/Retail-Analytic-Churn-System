Retail Intelligence & Churn Prediction System

📌 Overview

This project is an end-to-end data engineering and machine learning system designed to analyze customer behavior and predict churn. It automates data processing, builds customer insights using RFM analysis, trains predictive models, and delivers results through an interactive dashboard.

The goal is to move from raw data → insights → business decisions.

🏗️ Architecture

Airflow → Orchestrates the data pipeline
PostgreSQL → Stores structured data
Feature Engineering → RFM (Recency, Frequency, Monetary) metrics
Machine Learning → Churn prediction (Logistic Regression, XGBoost)
FastAPI → Serves model predictions via API
Streamlit → Interactive dashboard for insights and decision-making
Docker → Containerized environment for reproducibility
⚙️ Pipeline Flow

Data Generation & Ingestion

Simulated retail data is generated
Data is ingested into the pipeline
Data Validation

Schema checks (columns, types, nulls)
Ensures data quality before loading
Data Storage

Cleaned data is loaded into PostgreSQL
Feature Engineering

RFM metrics are computed:
Recency → Days since last purchase
Frequency → Number of orders
Monetary → Total spend
Model Training

Trains classification models to predict churn
Compares Logistic Regression and XGBoost
Saves best-performing model
Model Serving

FastAPI exposes prediction endpoint
Accepts input features and returns churn risk
Dashboard & Insights

Streamlit dashboard visualizes:
Customer segments
Revenue trends
Churn distribution
ML predictions
Business recommendations
📊 Key Features

Automated data pipeline using Airflow
Customer segmentation using RFM analysis
Machine learning churn prediction
Real-time prediction API (FastAPI)
Interactive multi-page dashboard (Streamlit)
Business insights and retention strategy simulation
Exportable reports (CSV)
Dockerized environment for reproducibility
📈 Dashboard Capabilities

Executive KPI overview
Customer segmentation (RFM visualization)
Churn risk analysis
Revenue and trend analysis
Top customer identification
ML-based churn prediction
Retention campaign simulation
Currency toggle ($ / ₦)
🚀 How to Run

Start Services (Docker)
docker-compose up -d

Run FastAPI (Model API)
uvicorn backend.api.main:app --reload

Run Streamlit Dashboard
streamlit run dashboard/app.py

Access Applications
Airflow → http://localhost:8080
API Docs → http://127.0.0.1:8000/docs
Dashboard → http://localhost:8501
🧠 Business Value

This system helps businesses:

Identify high-risk (churn) customers
Understand customer behavior and value
Track revenue trends and performance
Target customers with retention campaigns
Make data-driven decisions
🔍 Example Use Case

A business can:

Detect customers likely to churn
Offer discounts or incentives
Prioritize high-value customers
Optimize marketing strategies
🛠️ Tech Stack

Python
Pandas, NumPy
Scikit-learn, XGBoost
PostgreSQL
Apache Airflow
FastAPI
Streamlit
Docker
📌 Key Insight

This project demonstrates a full data-to-decision pipeline, where raw data is transformed into actionable insights and predictions that directly support business strategy.

💡 Summary

This is not just a dashboard — it is a complete data platform that integrates:

Data engineering
Analytics
Machine learning
API development
Business intelligence

👤 Author

Casmir Udeme
