import streamlit as st
from datetime import datetime

# ==========================
# HEADER
# ==========================

def show_header():

    left, right = st.columns([5,1])

    with left:
        st.title("🌍 Air Quality Monitoring Platform")
        st.caption("Real-Time Environmental Intelligence Dashboard")

    with right:
        st.success("🟢 LIVE")
        st.caption(datetime.now().strftime("%d %b %Y"))
        st.caption(datetime.now().strftime("%I:%M:%S %p"))

    st.divider()


# ==========================
# KPI CARD
# ==========================

def kpi_card(title, value, emoji, color):

    st.markdown(f"""
    <div style="
        background:{color};
        padding:22px;
        border-radius:18px;
        color:white;
        box-shadow:0 8px 20px rgba(0,0,0,.35);
        margin-bottom:10px;
    ">

<h4 style="margin:0;">
{emoji} {title}
</h4>

<h1 style="margin-top:15px;">
{value}
</h1>

</div>
""",
unsafe_allow_html=True)