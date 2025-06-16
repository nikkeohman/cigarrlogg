import sqlite3
import json
from datetime import datetime

conn = sqlite3.connect("cigarrdata.db")
cursor = conn.cursor()

# Hämta statistik
cursor.execute("SELECT period, avg_temp, min_temp, max_temp, avg_hum, min_hum, max_hum FROM statistics")
stats = cursor.fetchall()

statistics = {}
for row in stats:
    period, avg_t, min_t, max_t, avg_h, min_h, max_h = row
    statistics[period] = {
        "temperature": {
            "average": round(avg_t, 2),
            "min": round(min_t, 2),
            "max": round(max_t, 2)
        },
        "humidity": {
            "average": round(avg_h, 2),
            "min": round(min_h, 2),
            "max": round(max_h, 2)
        }
    }

# Hämta senaste logg
cursor.execute("SELECT timestamp, temperature, humidity FROM logg ORDER BY timestamp DESC LIMIT 1")
row = cursor.fetchone()
latest = {
    "timestamp": row[0],
    "temperature": round(row[1], 2),
    "humidity": round(row[2], 2)
}

# Skriv till JSON
output = {
    "generated_at": datetime.now().isoformat(),
    "latest": latest,
    "statistics": statistics
}

with open("docs/stats_data.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ stats_data.json generated.")

conn.close()
