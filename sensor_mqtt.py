from sense_hat import SenseHat
import paho.mqtt.client as mqtt
import json
from datetime import datetime
import time

sense = SenseHat()

BROKER = "localhost"
TOPIC = "environment/pi1"

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

device_id = "raspberrypi_1"

while True:
    temperature = sense.get_temperature()
    humidity = sense.get_humidity()
    pressure = sense.get_pressure()

    payload = {
        "device": device_id,
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "pressure": round(pressure, 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    message = json.dumps(payload)

    client.publish(TOPIC, message)

    print("Sent:", message)

    time.sleep(5)
