import sqlite3
from datetime import datetime, timedelta
import plotly.graph_objs as go
import plotly.io as pio
import json

# Read stats data
with open("docs/stats_data.json") as f:
    stats_data = json.load(f)

conn = sqlite3.connect("cigarrdata.db")
cursor = conn.cursor()

# Get latest measurement
cursor.execute("""
    SELECT timestamp, temperature, humidity, q.quote, q.author
    FROM logg l
    JOIN quotes q ON l.quote_id = q.id
    ORDER BY timestamp DESC
    LIMIT 1
""")
latest = cursor.fetchone()

latest_timestamp, latest_temp, latest_hum, latest_quote, latest_author = latest

# Function to get data for a given period
def get_data(days):
    period_ago = datetime.now() - timedelta(days=days)
    cursor.execute("""
        SELECT timestamp, temperature, humidity FROM logg
        WHERE timestamp >= ?
        ORDER BY timestamp ASC
    """, (period_ago.strftime("%Y-%m-%dT%H:%M:%S"),))
    return cursor.fetchall()

periods = {
    "Last 7 Days": 7,
    "Last 30 Days": 30,
    "Last Year": 365,
    "Last 5 Years": 365 * 5
}

figures = []

for title, days in periods.items():
    data = get_data(days)
    if not data:
        continue
    timestamps = [row[0] for row in data]
    temps = [row[1] for row in data]
    hums = [row[2] for row in data]

    # Calculate dynamic y-axis ranges
    temp_min = min(temps)
    temp_max = max(temps)
    hum_min = min(hums)
    hum_max = max(hums)

    temp_range = [min(temp_min, latest_temp - 5), max(temp_max, latest_temp + 5)]
    hum_range = [min(hum_min, latest_hum - 5), max(hum_max, latest_hum + 5)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=temps,
        mode='lines+markers',
        name="Temperature (°C)",
        line=dict(color="#FF7F0E"),
        yaxis="y1"
    ))
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=hums,
        mode='lines+markers',
        name="Humidity (%)",
        line=dict(color="#1F77B4"),
        yaxis="y2"
    ))
    fig.update_layout(
        title=title,
        xaxis=dict(title="Time"),
        yaxis=dict(title="Temperature (°C)", range=temp_range),
        yaxis2=dict(title="Humidity (%)", overlaying="y", side="right", range=hum_range),
        margin=dict(t=50, l=40, r=40, b=40),
        height=400
    )
    figures.append(pio.to_html(fig, full_html=False, include_plotlyjs=False))

cursor.close()
conn.close()

# Create HTML content
html = f"""
<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Humidor History</title>
    <link rel=\"icon\" href=\"favicon.ico\" type=\"image/x-icon\">
    <script src=\"https://cdn.plot.ly/plotly-2.32.0.min.js\"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f5f5f5; color: #333; }}
        header, footer {{ background: #222; color: white; padding: 1rem; text-align: center; }}
        main {{ padding: 2rem; max-width: 1000px; margin: auto; }}
        h2 {{ margin-top: 2rem; }}
        .quote {{ font-style: italic; margin: 2rem 0; text-align: center; }}
        .graph-container {{ margin-top: 2rem; }}
        #timestamp {{ font-size: 0.9em; color: #555; text-align: center; margin-bottom: 1rem; }}
    </style>
</head>
<body>
    <header>
        <h1>📈 Humidor History</h1>
    </header>
    <main>
        <div id=\"timestamp\">📅 Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        <section class=\"quote\">
            🗯️ \"{latest_quote}\"<br>— {latest_author}
        </section>
        <section class=\"graph-container\">
            {''.join(figures)}
        </section>
    </main>
    <footer>
        &copy; 2025 Cigarrlogg by Nikke Öhman
    </footer>
</body>
</html>
"""

# Write HTML to file
with open("docs/stats.html", "w") as f:
    f.write(html)

print("✅ stats.html generated.")

