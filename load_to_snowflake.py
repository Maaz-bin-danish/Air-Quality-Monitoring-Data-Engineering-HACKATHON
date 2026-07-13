import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


# Snowflake connection
conn = snowflake.connector.connect(
    user="MAAZDANISH",
    password="@Decentmaaz123",
    account="ppylmpv-fq49504",
    warehouse="AIR_QUALITY_WH",
    database="AIR_QUALITY_DB",
    schema="PUBLIC"
)

print("Connected Successfully!")


# CSV load
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

csv_path = os.path.join(BASE_DIR, "etl", "clean_iot_data.csv")

df = pd.read_csv(csv_path).tail(10)

df.columns = df.columns.str.upper()

print(df.head())


# Upload to Snowflake
success, nchunks, nrows, output = write_pandas(
    conn,
    df,
    "AIR_QUALITY"
)

print("Upload Status:", success)
print("Rows Inserted:", nrows)


conn.close()