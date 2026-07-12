import pandas as pd

# Read Simulator Data
simulator_df = pd.read_csv("../simulator/iot_readings.csv")

# Read OpenAQ Data
openaq_df = pd.read_csv("../api/openaq_locations.csv")

print("Simulator Data")
print(simulator_df.head())

print("\nOpenAQ Data")
print(openaq_df.head())

print("\nRows in Simulator:", len(simulator_df))
print("Rows in OpenAQ:", len(openaq_df))

# Remove duplicate rows
simulator_df = simulator_df.drop_duplicates()
openaq_df = openaq_df.drop_duplicates()

# Remove missing values
simulator_df = simulator_df.fillna("Unknown")
openaq_df = openaq_df.fillna("Unknown")

print("\nCleaning Completed Successfully!")

# Save cleaned files
simulator_df.to_csv("clean_iot_data.csv", index=False)
openaq_df.to_csv("clean_openaq_data.csv", index=False)

print("\nClean CSV Files Created Successfully!")