# README.md
# 🤻 Cigar Humidor Logger

A lightweight, cloud-synced monitoring tool for your cigar humidor — log temperature and humidity with a 1-Wire sensor, generate interactive graphs, and publish to a GitHub Pages website.

## 📦 Features

- Reads data from 1-Wire temperature and humidity sensors (e.g. DS2438 + SHT1x)
- Stores logs in a local SQLite database
- Visualizes data with interactive Plotly graphs
- Includes quote-of-the-day from a large cigar quote collection
- Publishes to GitHub Pages via a single shell script
- Easy to set up and extend

## 🔧 Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nikkeohman/cigarrlogg.git
   cd cigarrlogg
   ```

2. **Run the setup script (do not use sudo):**
   ```bash
   ./setup.sh
   ```

3. **Optional: Set up automatic logging via `cron`.**
   Example to log every 10 minutes:
   ```bash
   crontab -e
   ```
   Add:
   ```cron
   */10 * * * * /home/youruser/cigarrlogg/update.sh >> /home/youruser/cigarrlogg/cron.log 2>&1
   ```

4. **Your site will be generated in the `docs/` folder.**
   Enable GitHub Pages in your repo settings with `docs/` as the source.

## 🔁 Updating

To manually log and update:
```bash
./update.sh
```

## 📂 Project Structure

- `log_cigarr.py` – reads sensor data and stores it in `cigarrdata.db`
- `generate_html.py` – creates an interactive web page with latest and historical data
- `quotes_with_authors.json` – your quote collection
- `docs/index.html` – generated output for GitHub Pages
- `update.sh` – logs, generates HTML, commits and pushes

## 🧠 Data Insights

- The homepage displays the latest temperature and humidity readings.
- Charts include trends over time, and summaries of min/avg/max for day, week, month, year.
- Data is stored locally in a SQLite database.

## 📜 Requirements

- Raspberry Pi or Linux with 1-Wire support (e.g. DS9490R USB adapter)
- Python 3.9+
- GitHub account for publishing

## 🤝 Contributions

Feel free to fork and improve! Pull requests welcome — especially for:

- New features (e.g. alerts, export, more sensors)
- Design/UI improvements
- More cigar quotes!

## 📃 License

MIT License
