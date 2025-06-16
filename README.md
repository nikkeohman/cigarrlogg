# Cigarrlogg

This project logs temperature and humidity in a cigar humidor using 1-Wire sensors on a Raspberry Pi, stores the data in a SQLite database, and generates a stylish HTML dashboard with charts and cigar quotes. Everything is automatically deployed to GitHub Pages.

## Features

- 🕒 Timestamps, 🌡️ Temperature, 💧 Humidity
- 📜 Random cigar quotes stored in the database
- 📈 Historical data shown as interactive Plotly charts
- 🧠 Logs new data and generates HTML with a single script
- ☁️ Hosted on GitHub Pages for free public access

## Repository Structure

```
├── cigarrdata.db          # SQLite database
├── docs/
│   └── index.html         # Generated HTML page
├── log_cigarr.py          # Script for logging sensor data
├── generate_html.py       # Script for generating HTML from database
├── quotes.txt             # Optional: quotes to import
├── update.sh              # Runs both scripts and pushes to GitHub
├── README.md              # You're reading this
```

## Requirements

- Python 3
- Plotly
- SQLite3
- Git

## Setup (on Raspberry Pi)

1. Clone the repository:
   ```bash
   git clone https://github.com/nikkeohman/cigarrlogg.git
   cd cigarrlogg
   ```
2. Create a Python virtual environment:
   ```bash
   python3 -m venv ~/cigarr-venv
   source ~/cigarr-venv/bin/activate
   pip install plotly
   ```
3. Add your GitHub token to `.netrc` (for automated pushes):
   ```bash
   machine github.com
     login <your_username>
     password <your_token>
   ```
4. Set up crontab:
   ```bash
   crontab -e
   # Add the following line:
   */60 * * * * cd /home/pi/cigarrlogg && ./update.sh
   ```

## Example Output

![screenshot](docs/screenshot.png)

## License

MIT License — feel free to fork and improve!
