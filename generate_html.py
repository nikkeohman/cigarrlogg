import sqlite3
import plotly.graph_objects as go
from datetime import datetime

# Läs data
conn = sqlite3.connect("cigarrdata.db")
cursor = conn.cursor()
cursor.execute("SELECT timestamp, temperature, humidity FROM cigar_log ORDER BY timestamp")
rows = cursor.fetchall()
conn.close()

# Omvandla
timestamps = [datetime.fromisoformat(r[0]) for r in rows]
temps = [r[1] for r in rows]
humidity = [r[2] for r in rows]

# Skapa grafer
fig = go.Figure()
fig.add_trace(go.Scatter(x=timestamps, y=temps, mode='lines+markers', name='Temp (°C)'))
fig.add_trace(go.Scatter(x=timestamps, y=humidity, mode='lines+markers', name='Fuktighet (%)'))
fig.update_layout(title="Humidorövervakning", xaxis_title="Tid", yaxis_title="Värde")

# Exportera till HTML
fig.write_html("docs/index.html", full_html=True, include_plotlyjs="cdn")
print("✅ HTML-sida genererad: docs/index.html")
