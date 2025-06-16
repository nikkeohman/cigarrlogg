# log_cigarr.py

import sqlite3
import random
from datetime import datetime

DB_PATH = "cigarrdata.db"

def read_sensor_data():
    # Läs från dina 1-wire-sensorer (mockad här som exempel)
    with open("/mnt/1wire/26.E4E5F1000000/humidity", "r") as f:
        humidity = float(f.read())
    with open("/mnt/1wire/26.E4E5F1000000/temperature", "r") as f:
        temperature = float(f.read())
    return temperature, humidity

def get_random_quote_id_and_text(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT id, quote FROM quotes ORDER BY RANDOM() LIMIT 1")
    return cursor.fetchone()

def log_data():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    timestamp = datetime.now().isoformat(timespec='seconds')
    temperature, humidity = read_sensor_data()
    quote_id, quote = get_random_quote_id_and_text(conn)

    cursor.execute(
        "INSERT INTO logg (timestamp, temperature, humidity, quote_id) VALUES (?, ?, ?, ?)",
        (timestamp, temperature, humidity, quote_id)
    )

    conn.commit()
    conn.close()

    print(f"🕒 {timestamp}")
    print(f"🌡️ Temp: {temperature:.2f} °C")
    print(f"💧 Fuktighet: {humidity:.2f} %")
    print(f"🗯️ \"{quote}\"")

if __name__ == "__main__":
    log_data()
