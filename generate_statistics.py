import sqlite3
from datetime import datetime, timedelta

# Öppna databasen
conn = sqlite3.connect("cigarrdata.db")
cursor = conn.cursor()

# Skapa tabellen om den inte finns
cursor.execute("""
CREATE TABLE IF NOT EXISTS statistics (
    period TEXT PRIMARY KEY,
    avg_temp REAL,
    min_temp REAL,
    max_temp REAL,
    latest_temp REAL,
    avg_hum REAL,
    min_hum REAL,
    max_hum REAL,
    latest_hum REAL
)
""")

# Rensa gammal data
cursor.execute("DELETE FROM statistics")

# Definiera tidsintervaller
periods = {
    "Last 24 hours": timedelta(days=1),
    "Last 7 days": timedelta(days=7),
    "Last 30 days": timedelta(days=30),
    "Last 365 days": timedelta(days=365),
}

now = datetime.utcnow()

for label, delta in periods.items():
    since = now - delta
    since_iso = since.isoformat()

    # Temperatur och fuktighet: medel, min, max
    cursor.execute("""
        SELECT 
            AVG(temperature), MIN(temperature), MAX(temperature),
            AVG(humidity), MIN(humidity), MAX(humidity)
        FROM logg
        WHERE timestamp >= ?
    """, (since_iso,))
    avg_temp, min_temp, max_temp, avg_hum, min_hum, max_hum = cursor.fetchone()

    # Senaste mätning
    cursor.execute("""
        SELECT temperature, humidity 
        FROM logg 
        WHERE timestamp >= ? 
        ORDER BY timestamp DESC 
        LIMIT 1
    """, (since_iso,))
    latest = cursor.fetchone() or (None, None)
    latest_temp, latest_hum = latest

    # Spara i statistics-tabellen
    cursor.execute("""
        INSERT INTO statistics (
            period, avg_temp, min_temp, max_temp, latest_temp,
            avg_hum, min_hum, max_hum, latest_hum
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        label, avg_temp, min_temp, max_temp, latest_temp,
        avg_hum, min_hum, max_hum, latest_hum
    ))

conn.commit()
conn.close()
print("✅ Statistics updated.")
