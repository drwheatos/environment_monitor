import paho.mqtt.client as mqtt
import sqlite3
import json

#import above libraries

# database set up 

#connect to SQLite db
conn = sqlite3.connect("environment.db")
cursor = conn.cursor()

#creat table if it doesn’t exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device TEXT,
    temperature REAL,
    humidity REAL,
    pressure REAL,
    timestamp TEXT
)
""")

# alerts table 
cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
id INTEGER PRIMARY KEY AUTOINCREMENT,
message TEXT,
timestamp TEXT
)
""")


# save db changes
conn.commit()


# MQTT settings


BROKER = "localhost"
TOPIC = "environment/pi1"

# temperature threshold
TEMPERATURE_THRESHOLD = 22


# helper functions

def get_average_temperature():

    cursor.execute("SELECT AVG(temperature) FROM readings")
    result = cursor.fetchone()[0]

    return round(result, 2) if result else 0

# When message received


def on_message(client, userdata, msg):

#convert message
    payload = msg.payload.decode()
#print
    print(f"Received: {payload}")
#convert JSON string to python dictionary
    data = json.loads(payload)

#insert sensor data to db
    cursor.execute("""
    INSERT INTO readings (
        device,
        temperature,
        humidity,
        pressure,
        timestamp
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["device"],
        data["temperature"],
        data["humidity"],
        data["pressure"],
        data["timestamp"]
    ))

#sava data
    conn.commit()

    print("Data saved to database.")


# MQTT client

#create
client = mqtt.Client()
#set message callback
client.on_message = on_message
#connect broker
client.connect(BROKER, 1883, 60)

client.subscribe(TOPIC)

#print status message
print("Subscriber running...")

#keep running and checking for messages
client.loop_forever()
