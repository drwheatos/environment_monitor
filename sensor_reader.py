from sense_hat import SenseHat
import time
import csv
from datetime import datetime

sense = SenseHat()

TEMP_THRESHOLD = 30

while True:

    temp = round(sense.get_temperature(), 2)
    humidity = round(sense.get_humidity(), 2)
    pressure = round(sense.get_pressure(), 2)

    timestamp = datetime.now()

    print(f"\n[{timestamp}]")
    print(f"Temperature: {temp} C")
    print(f"Humidity: {humidity}%")
    print(f"Pressure: {pressure} mb")

    if temp > TEMP_THRESHOLD:
        print("WARNING: High temperature detected!")

    with open("sensor_log.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, temp, humidity, pressure])

    time.sleep(5)
