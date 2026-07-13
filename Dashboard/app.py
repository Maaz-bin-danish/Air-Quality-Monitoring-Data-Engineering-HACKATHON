
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from streamlit_autorefresh import st_autorefresh
from config import AUTO_REFRESH
from data_loader import load_data
from components import show_header, kpi_card

print("APP STARTED")

# ---------------- PAGE ----------------

st.set_page_config(
    page_title="Air Quality Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st_autorefresh(interval=AUTO_REFRESH, key="refresh")

st.toast(
    "🟢 Connected to Snowflake | Auto Refresh every 10 seconds",
    icon="✅"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- HEADER ----------------

show_header()

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "📊 Dashboard",
        "📈 Analytics",
        "🌡 Sensors",
        "📋 Raw Data"
    ]
)

# ---------------- DATA ----------------

df = load_data()

latest_df = (
    df.sort_values("RECORDED_AT")
      .tail(10)
)

avg_aqi = round(latest_df["AQI"].mean(), 2)
avg_pm25 = round(latest_df["PM25"].mean(), 2)
avg_co2 = round(latest_df["CO2"].mean(), 2)

# ---------------- SIDEBAR ----------------

st.sidebar.title("🌍 Dashboard Filters")
st.sidebar.markdown("---")

cities = st.sidebar.multiselect(
    "🏙️ Select City",
    sorted(df["CITY"].unique()),
    default=sorted(df["CITY"].unique())
)

severity = st.sidebar.multiselect(
    "🚨 Select Severity",
    sorted(df["SEVERITY"].unique()),
    default=sorted(df["SEVERITY"].unique())
)

zones = st.sidebar.multiselect(
    "📍 Select Zone",
    sorted(df["ZONE"].unique()),
    default=sorted(df["ZONE"].unique())
)

df = df[
    (df["CITY"].isin(cities))
    &
    (df["SEVERITY"].isin(severity))
    &
    (df["ZONE"].isin(zones))
]

st.sidebar.markdown("---")
st.sidebar.success(f"Showing {len(df)} records")

# ====================================================
# KPI SECTION
# ====================================================


st.markdown("## 📊 Dashboard Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    kpi_card(
        "Total Records",
        len(df),
        "📄",
        "linear-gradient(135deg,#2563EB,#1E3A8A)"
    )

with c2:
    kpi_card(
        "Average AQI",
        avg_aqi,
        "🌫",
        "linear-gradient(135deg,#16A34A,#166534)"
    )

with c3:
    kpi_card(
        "Average PM2.5",
        avg_pm25,
        "💨",
        "linear-gradient(135deg,#F97316,#C2410C)"
    )

with c4:
    kpi_card(
        "Average CO₂",
        avg_co2,
        "🏭",
        "linear-gradient(135deg,#DC2626,#991B1B)"
    )

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("## 🌍 Air Quality Status")

left, right = st.columns([1, 2])

with left:

    avg_aqi = round(df["AQI"].mean(), 2)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_aqi,
        title={'text': "Average AQI"},
        gauge={
            'axis': {'range': [0, 200]},
            'bar': {'color': "#00E5FF"},
            'steps': [
                {'range': [0, 50], 'color': "#22C55E"},
                {'range': [50, 100], 'color': "#EAB308"},
                {'range': [100, 150], 'color': "#F97316"},
                {'range': [150, 200], 'color': "#DC2626"},
            ]
        }
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        font_color="white",
        height=350,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    st.markdown("### 📌 Air Quality Insights")

    city_aqi = df.groupby("CITY")["AQI"].mean()

    highest_city = city_aqi.idxmax()
    highest_value = round(city_aqi.max(), 2)

    lowest_city = city_aqi.idxmin()
    lowest_value = round(city_aqi.min(), 2)

    col1, col2 = st.columns(2)

    with col1:
        st.success(
            f"""
### 🌿 Cleanest City

**{lowest_city}**

AQI: **{lowest_value}**
"""
        )

    with col2:
        st.error(
            f"""
### ☣ Most Polluted

**{highest_city}**

AQI: **{highest_value}**
"""
        )

    st.info(
        f"""
### 🌡 Highest Temperature

**{df['TEMPERATURE'].max()} °C**
"""
    )

    st.warning(
        f"""
### 💧 Average Humidity

**{round(df['HUMIDITY'].mean(),1)} %**
"""
    )

# ====================================================
# AQI TREND
# ====================================================

st.markdown("## 📈 AQI Trend")

fig = px.line(
    df,
    x="RECORDED_AT",
    y="AQI",
    color="CITY",
    markers=True
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#111827",
    plot_bgcolor="#111827",
    font_color="white",
    height=450
)

st.plotly_chart(fig, use_container_width=True)

# ====================================================
# ANALYTICS
# ====================================================

st.markdown("## 📊 Analytics")

left, right = st.columns(2)

with left:

    fig = px.bar(
        df.groupby("CITY")["AQI"].mean().reset_index(),
        x="CITY",
        y="AQI",
        color="CITY",
        text_auto=".1f"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        height=420,
        title="Average AQI by City"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.pie(
        df,
        names="SEVERITY",
        hole=.65
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        font_color="white",
        height=420,
        title="Severity Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ====================================================
# POLLUTION
# ====================================================

st.markdown("## 🌫 Pollution Analysis")

left, right = st.columns(2)

with left:

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
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    fig = px.scatter(
        df,
        x="TEMPERATURE",
        y="HUMIDITY",
        color="CITY",
        size="AQI",
        hover_name="SENSOR_ID"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

# ====================================================
# TABLE
# ====================================================

st.markdown("## 📋 Latest Sensor Readings")

st.dataframe(
    df,
    use_container_width=True,
    height=400
)

# ====================================================
# DOWNLOAD
# ====================================================

st.markdown("### ⬇ Export Data")

csv = df.to_csv(index=False)

st.download_button(
    "📥 Download CSV",
    csv,
    file_name="air_quality.csv",
    mime="text/csv",
    use_container_width=True
)