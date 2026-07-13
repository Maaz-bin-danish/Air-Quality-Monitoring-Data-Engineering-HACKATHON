import random
import datetime
import time
import csv
import os
import subprocess

# -------------------------------
# Sensor List
# -------------------------------
sensors = [
    {"sensor_id": "PKS_KHI_IND_01", "city": "Karachi", "zone": "Industrial"},
    {"sensor_id": "PKS_KHI_TRF_02", "city": "Karachi", "zone": "Traffic"},
    {"sensor_id": "PKS_LHR_RES_01", "city": "Lahore", "zone": "Residential"},
    {"sensor_id": "PKS_LHR_IND_02", "city": "Lahore", "zone": "Industrial"},
    {"sensor_id": "PKS_ISB_PRK_01", "city": "Islamabad", "zone": "Park"},
    {"sensor_id": "PKS_ISB_TRF_02", "city": "Islamabad", "zone": "Traffic"},
    {"sensor_id": "PKS_PEW_IND_01", "city": "Peshawar", "zone": "Industrial"},
    {"sensor_id": "PKS_PEW_RES_02", "city": "Peshawar", "zone": "Residential"},
    {"sensor_id": "PKS_MUL_TRF_01", "city": "Multan", "zone": "Traffic"},
    {"sensor_id": "PKS_MUL_PRK_02", "city": "Multan", "zone": "Park"}
]

# -------------------------------
# Create CSV File
# -------------------------------
file_exists = os.path.exists("iot_readings.csv")

file = open("iot_readings.csv", "a", newline="")

writer = csv.writer(file)

if not file_exists:
    writer.writerow([
        "sensor_id",
        "city",
        "zone",
        "pm25",
        "pm10",
        "co2",
        "temperature",
        "humidity",
        "wind_speed",
        "aqi",
        "severity",
        "recorded_at"
    ])

print("Smart City Air Quality Simulator Started...")
print("=" * 60)

while True:

    print("\n================ NEW BATCH ================\n")

    for sensor in sensors:

        zone = sensor["zone"]

        # Generate values according to zone
        if zone == "Industrial":
            pm25 = random.randint(80, 120)
            co2 = random.randint(600, 900)
            temperature = random.randint(30, 42)

        elif zone == "Traffic":
            pm25 = random.randint(55, 80)
            co2 = random.randint(500, 700)
            temperature = random.randint(28, 40)

        elif zone == "Residential":
            pm25 = random.randint(25, 50)
            co2 = random.randint(420, 500)
            temperature = random.randint(25, 38)

        else:  # Park
            pm25 = random.randint(8, 20)
            co2 = random.randint(400, 430)
            temperature = random.randint(22, 35)

        # Other values
        pm10 = random.randint(pm25, pm25 + 100)
        humidity = random.randint(20, 90)
        wind_speed = random.randint(0, 60)

        # Temporary AQI
        aqi = pm25

        # Severity
        if aqi <= 50:
            severity = "GOOD"
        elif aqi <= 100:
            severity = "MODERATE"
        elif aqi <= 150:
            severity = "UNHEALTHY"
        else:
            severity = "HAZARDOUS"

        current_time = datetime.datetime.now()

        # Print Data
        print("------------------------------------------")
        print("Sensor ID    :", sensor["sensor_id"])
        print("City         :", sensor["city"])
        print("Zone         :", sensor["zone"])
        print("PM2.5        :", pm25)
        print("PM10         :", pm10)
        print("CO2          :", co2)
        print("Temperature  :", temperature, "°C")
        print("Humidity     :", humidity, "%")
        print("Wind Speed   :", wind_speed, "km/h")
        print("AQI          :", aqi)
        print("Severity     :", severity)
        print("Recorded At  :", current_time)

        # Save to CSV
        writer.writerow([
            sensor["sensor_id"],
            sensor["city"],
            sensor["zone"],
            pm25,
            pm10,
            co2,
            temperature,
            humidity,
            wind_speed,
            aqi,
            severity,
            current_time
        ])

        file.flush()
    print("Running ETL...")
    subprocess.run(["python", "../etl/etl.py"])

    print("Uploading to Snowflake...")
    subprocess.run(["python", "../load_to_snowflake.py"])

    print("\nWaiting 10 seconds for next batch...\n")
    time.sleep(10)