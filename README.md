# 🌍 Smart City Air Quality Monitoring Dashboard

## 📌 Overview

This project is a real-time Air Quality Monitoring Dashboard developed for the SMIT Data Engineering Hackathon.

The system simulates IoT air quality sensors, processes the data through an ETL pipeline, stores it in Snowflake Data Warehouse, and visualizes it using Streamlit.

---

## 🚀 Features

- Real-time IoT sensor simulation
- Automatic data generation every 10 seconds
- ETL data cleaning process
- Snowflake Cloud Data Warehouse
- Interactive Streamlit Dashboard
- Auto-refresh every 10 seconds
- Dynamic KPIs
- AQI Trends
- Pollution Analytics
- Sensor Data Table
- CSV Export

---

## 🛠 Technologies Used

- Python
- Pandas
- Streamlit
- Snowflake
- Plotly
- SQL

---

## 📂 Project Structure

```
Project/
│
├── simulator/
│   └── simulator.py
│
├── etl/
│   └── etl.py
│
├── dashboard/
│   ├── app.py
│   ├── data_loader.py
│   ├── components.py
│   ├── config.py
│   └── style.css
│
├── load_to_snowflake.py
└── README.md
```

---

## 🔄 Workflow

IoT Simulator

↓

CSV Generation

↓

ETL Cleaning

↓

Snowflake Data Warehouse

↓

Streamlit Dashboard

---

## 📊 Dashboard Features

- Live AQI Monitoring
- Average AQI
- Average PM2.5
- Average CO₂
- Air Quality Gauge
- City-wise AQI Analysis
- Severity Distribution
- Pollution Analysis
- Sensor Readings Table

---

## 👨‍💻 Developed By

**Maaz Danish**

SMIT Data Engineering Hackathon Project