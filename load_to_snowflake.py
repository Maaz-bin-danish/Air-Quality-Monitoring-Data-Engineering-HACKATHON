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
df = pd.read_csv("etl/clean_iot_data.csv")

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