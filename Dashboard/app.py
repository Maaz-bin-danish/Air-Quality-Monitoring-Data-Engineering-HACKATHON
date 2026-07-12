import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector

from streamlit_autorefresh import st_autorefresh

# ---------------- PAGE ----------------
st.set_page_config(
    page_title="Air Quality Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


st_autorefresh(interval=10000,key="refresh")

# with open("style.css") as f:
#     st.markdown(
#         f"<style>{f.read()}</style>",
#         unsafe_allow_html=True
#     )

st.markdown("""
<h1 style='text-align:center;color:white;'>
🌍 Air Quality Monitoring Dashboard
</h1>

<h3 style='text-align:center;color:#38BDF8;'>
Real-Time Air Pollution Analytics
</h3>
""",unsafe_allow_html=True)

# ---------------- SNOWFLAKE ----------------
conn = snowflake.connector.connect(
    user="MAAZDANISH",
    password="@Decentmaaz123",
    account="ppylmpv-fq49504",
    warehouse="AIR_QUALITY_WH",
    database="AIR_QUALITY_DB",
    schema="PUBLIC"
)

query = "SELECT * FROM AIR_QUALITY"

cur = conn.cursor()
cur.execute(query)

df = cur.fetch_pandas_all()

conn.close()

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌍 Dashboard Filters")
st.sidebar.markdown("---")

cities = st.sidebar.multiselect(
    "🏙️ Select City",
    options=sorted(df["CITY"].unique()),
    default=sorted(df["CITY"].unique())
)

severity = st.sidebar.multiselect(
    "🚨 Select Severity",
    options=sorted(df["SEVERITY"].unique()),
    default=sorted(df["SEVERITY"].unique())
)

selected_zone = st.sidebar.multiselect(
    "📍 Select Zone",
    options=sorted(df["ZONE"].unique()),
    default=sorted(df["ZONE"].unique())
)

df = df[
    (df["CITY"].isin(cities)) &
    (df["SEVERITY"].isin(severity)) &
    (df["ZONE"].isin(selected_zone))
]

st.sidebar.markdown("---")
st.sidebar.success(f"Showing {len(df)} records")
# ---------------- KPI ----------------
st.markdown("---")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Total Records",
    len(df)
)

c2.metric(
    "Average AQI",
    round(df["AQI"].mean(),2)
)

c3.metric(
    "Average PM2.5",
    round(df["PM25"].mean(),2)
)

c4.metric(
    "Average CO2",
    round(df["CO2"].mean(),2)
)

st.markdown("---")


# ---------------- AQI TREND ----------------

st.subheader("AQI Trend")

fig = px.line(
    df,
    x="RECORDED_AT",
    y="AQI",
    color="CITY"
)
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F172A",
    plot_bgcolor="#0F172A",
    font_color="white"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------- CITY ----------------

left,right = st.columns(2)

with left:

    st.subheader("Average AQI by City")

    fig = px.bar(
        df.groupby("CITY")["AQI"].mean().reset_index(),
        x="CITY",
        y="AQI",
        color="CITY"
    )

    fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F172A",
    plot_bgcolor="#0F172A",
    font_color="white"
)

    st.plotly_chart(fig,use_container_width=True)

with right:

    st.subheader("🚨 Severity Distribution")

    fig = px.pie(
        df,
        names="SEVERITY",
        hole=0.6
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        font_color="white",
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)
# ---------------- POLLUTION ----------------

st.subheader("Pollution Comparison")

fig = px.scatter(
    df,
    x="PM25",
    y="PM10",
    color="CITY",
    size="AQI",
    hover_name="SENSOR_ID"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0F172A",
    plot_bgcolor="#0F172A",
    font_color="white"
)

st.plotly_chart(fig,use_container_width=True)

# ---------------- TABLE ----------------

st.subheader("🌡️ Temperature vs Humidity")

fig = px.scatter(
    df,
    x="TEMPERATURE",
    y="HUMIDITY",
    color="CITY",
    size="AQI",
    hover_name="SENSOR_ID"
)

fig.update_layout(template="plotly_dark")

st.plotly_chart(fig, use_container_width=True)

st.subheader("Latest Sensor Readings")

st.dataframe(df)

# ---------------- DOWNLOAD ----------------

csv = df.to_csv(index=False)

st.download_button(
    "Download CSV",
    csv,
    "air_quality.csv",
    "text/csv"
)