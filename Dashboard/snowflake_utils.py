import snowflake.connector
import pandas as pd
import streamlit as st


@st.cache_data(ttl=10)
def load_data():

    conn = snowflake.connector.connect(
        user="MAAZDANISH",
        password="@Decentmaaz123",
        account="ppylmpv-fq49504",
        warehouse="AIR_QUALITY_WH",
        database="AIR_QUALITY_DB",
        schema="PUBLIC"
    )

    query = """
    SELECT *
    FROM AIR_QUALITY
    ORDER BY RECORDED_AT DESC
    """

    df = pd.read_sql(query, conn)

    conn.close()

    return df