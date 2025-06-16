# README.md
# 🌬️ Cigar Humidor Logger

A lightweight, cloud-synced monitoring tool for your cigar humidor — log temperature and humidity with a 1-Wire sensor, generate interactive graphs, and publish to a modern GitHub Pages website.

## 📦 Features

- 🔌 Reads data from 1-Wire temperature and humidity sensors (e.g. DS2438 + SHT1x)
- 📊 Interactive charts with Plotly
- 🧠 Local SQLite database with historical data and statistics
- 🛨️ Quote-of-the-day from a curated cigar quote collection
- 🌐 Publishes to GitHub Pages
- 🛠️ One-line setup with `setup.sh`

## 🚀 Quick Start

```bash
git clone https://github.com/nikkeohman/cigarrlogg.git
cd cigarrlogg
./setup.sh
```

## ⏱️ Automation

Enable automatic logging every 10 minutes via cron:

```bash
crontab -e
```
Add:
```cron
*/10 * * * * /home/youruser/cigarrlogg/update.sh >> /home/youruser/cigarrlogg/cron.log 2>&1
```

## 📂 Project Layout

- `log_cigarr.py` – log sensor data
- `generate_html.py` – build interactive website
- `quotes_with_authors.json` – cigar quote collection
- `docs/index.html` – published web output
- `docs/stats.html` – detailed statistics
- `update.sh` – automation script
- `setup.sh` – install everything in one go
- `cigarrdata.db` – SQLite database

## 🧠 Insights on the Site

- ✅ Latest temperature and humidity at the top
- 📈 Graphs for trends
- 📉 Min, Max, Average stats for: 24h, 7d, 30d, 365d
- 📜 Quotes include author attribution
- 🌐 [New] Dedicated statistics page with historical trends

## 🌐 Publishing

Make sure your GitHub repo has GitHub Pages enabled with:
```
/docs
```
as the publishing folder.

## 📜 Requirements

- Raspberry Pi or Linux machine with 1-Wire support
- Python 3.9+
- GitHub account

## 🎨 Roadmap Ideas

- Modern dark/light UI switch
- Mobile-friendly layout
- Export to CSV or JSON
- Cigar inventory management
- Alerts (email, Telegram, Discord)

## 🤝 Contributions

PRs are welcome! Improvements to:

- UI and layout
- More cigar quotes
- Feature requests

## 🪪 License

MIT License — Enjoy responsibly.
