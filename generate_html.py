# generate_html.py

import sqlite3
from datetime import datetime

DB_PATH = "cigarrdata.db"
HTML_PATH = "docs/index.html"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get latest reading
cursor.execute("""
    SELECT timestamp, temperature, humidity, quote, author
    FROM logg l
    JOIN quotes q ON l.quote_id = q.id
    ORDER BY timestamp DESC
    LIMIT 1
""")
latest = cursor.fetchone()
latest_time, latest_temp, latest_hum, latest_quote, latest_author = latest

# Get recent logs for graph
cursor.execute("""
    SELECT timestamp, temperature, humidity
    FROM logg
    ORDER BY timestamp DESC
    LIMIT 100
""")
data = cursor.fetchall()
data.reverse()
timestamps = [row[0] for row in data]
temperatures = [row[1] for row in data]
humidities = [row[2] for row in data]

# Get Ωstatistics
cursor.execute("""
    SELECT period, avg_temp, min_temp, max_temp, avg_hum, min_hum, max_hum
    FROM statistics
    ORDER BY
        CASE period
            WHEN '24h' THEN 1
            WHEN '7d' THEN 2
            WHEN '30d' THEN 3
            WHEN '365d' THEN 4
            ELSE 5
        END
""")
stats = cursor.fetchall()

conn.close()

with open(HTML_PATH, "w") as f:
    f.write(f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Cigar Humidor Log</title>
  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
  <style>
    body {{
      font-family: 'Segoe UI', sans-serif;
      margin: 0;
      padding: 1rem;
      background-color: #f8f8f8;
      color: #333;
    }}
    header {{
      text-align: center;
      margin-bottom: 2rem;
    }}
    h1 {{
      font-size: 2rem;
      margin-bottom: 0.2rem;
    }}
    .quote {{
      font-style: italic;
      text-align: center;
      margin-bottom: 1rem;
    }}
    .reading {{
      text-align: center;
      margin-bottom: 1rem;
    }}
    .chart-container {{
      max-width: 900px;
      margin: 0 auto 2rem auto;
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1rem;
      max-width: 900px;
      margin: 2rem auto;
      background: #fff;
      padding: 1rem;
      border-radius: 0.5rem;
      box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }}
    .stat-block {{
      border-left: 4px solid #555;
      padding-left: 1rem;
    }}
    footer {{
      text-align: center;
      font-size: 0.9rem;
      margin-top: 2rem;
      color: #666;
    }}
  </style>
</head>
<body>
  <header>
    <h1>🌬️ Cigar Humidor</h1>
    <div class="quote">“{latest_quote}”<br>– {latest_author}</div>
    <div class="reading">
      <strong>🕒 {latest_time}</strong><br>
      🌡️ {latest_temp:.2f} °C<br>
      💧 {latest_hum:.2f} %
    </div>
  </header>

  <div class="chart-container">
    <div id="temp-chart"></div>
    <div id="hum-chart"></div>
  </div>

  <section class="stats">
""")
    for period, avg_t, min_t, max_t, avg_h, min_h, max_h in stats:
        f.write(f"""
    <div class="stat-block">
      <h3>{period}</h3>
      <p>🌡️ Temp: {avg_t:.1f}° avg, {min_t:.1f}° min, {max_t:.1f}° max</p>
      <p>💧 Humidity: {avg_h:.1f}% avg, {min_h:.1f}% min, {max_h:.1f}% max</p>
    </div>
""")

    f.write(f"""
  </section>

  <footer>
    Last updated: {datetime.now().isoformat(sep=' ', timespec='seconds')}<br>
    <a href="stats.html">📈 View full statistics</a>
  </footer>

  <script>
    const tempTrace = {{
      x: {timestamps},
      y: {temperatures},
      mode: 'lines+markers',
      name: 'Temperature',
      line: {{color: 'red'}},
    }};
    Plotly.newPlot('temp-chart', [tempTrace], {{
      title: 'Temperature (°C)',
      xaxis: {{ title: 'Timestamp' }},
      yaxis: {{ title: '°C' }}
    }});

    const humTrace = {{
      x: {timestamps},
      y: {humidities},
      mode: 'lines+markers',
      name: 'Humidity',
      line: {{color: 'blue'}},
    }};
    Plotly.newPlot('hum-chart', [humTrace], {{
      title: 'Humidity (%)',
      xaxis: {{ title: 'Timestamp' }},
      yaxis: {{ title: '%' }}
    }});
  </script>
</body>
</html>
""")

