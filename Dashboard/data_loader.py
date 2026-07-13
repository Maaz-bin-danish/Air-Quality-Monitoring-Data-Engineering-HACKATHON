# ==========================================================
# DATA LOADER
# Responsible for fetching data from Snowflake
# ==========================================================

import streamlit as st
import snowflake.connector
import pandas as pd

from config import SNOWFLAKE_CONFIG



def load_data():

    print("1. Starting Snowflake connection")

    conn = snowflake.connector.connect(**SNOWFLAKE_CONFIG)

    print("2. Snowflake connected")

    query = """
    SELECT *
    FROM AIR_QUALITY_DB.PUBLIC.AIR_QUALITY
    """

    print("3. Running query")

    cursor = conn.cursor()
    cursor.execute(query)

    print("4. Query executed")

    df = cursor.fetch_pandas_all()

    print("5. Data received:", df.shape)

    conn.close()

    return df

