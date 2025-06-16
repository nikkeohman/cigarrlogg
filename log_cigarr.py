#!/usr/bin/env python3

import os
import time
import random
import sqlite3
from datetime import datetime

# VÄGAR TILL OWFS-FILER (anpassa om dina adresser ändras)
TEMPERATURE_PATH = "/mnt/1wire/26.E4E5F1000000/temperature"
HUMIDITY_PATH = "/mnt/1wire/26.E4E5F1000000/humidity"

# CIGARR-CITAT
QUOTES = [
    "Cigars are the perfect complement to life's contemplative moments.",
    "A good cigar is as great a comfort to a man as a good cry to a woman.",
    "A cigar numbs sorrow and fills the solitary hours with a million gracious images.",
    "I have made it a rule never to smoke more than one cigar at a time.",
    "Eating and sleeping are the only activities that should be allowed to interrupt a man's enjoyment of his cigar."
]

# HÄMTA MÄTVÄRDE
def read_value(path):
    try:
        with open(path, "r") as f:
            return float(f.read().strip())
    except Exception as e:
        print(f"⚠️ Error reading {path}: {e}")
        return None

# SKAPA DB (om den inte finns)
def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cigar_log (
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            quote TEXT
        );
    """)
    conn.commit()

# HUVUDLOGIK
def main():
    temp = read_value(TEMPERATURE_PATH)
    humidity = read_value(HUMIDITY_PATH)
    quote = random.choice(QUOTES)
    timestamp = datetime.now().isoformat(timespec='seconds')

    if temp is None or humidity is None:
        print("⚠️ Temp/fuktighet kunde inte läsas.")
        return

    # Logga till terminalen
    print(f"🕒 {timestamp}")
    print(f"🌡️ Temp: {temp:.2f} °C")
    print(f"💧 Fuktighet: {humidity:.2f} %")
    print(f"🗯️ \"{quote}\"")

    # Spara till SQLite
    conn = sqlite3.connect("cigarrdata.db")
    init_db(conn)
    conn.execute("INSERT INTO cigar_log VALUES (?, ?, ?, ?);",
                 (timestamp, temp, humidity, quote))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
