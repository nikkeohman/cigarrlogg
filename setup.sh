#!/bin/bash

echo "🔧 Starting setup..."

# Kontrollera att vi kör som rätt användare
if [ "$EUID" -eq 0 ]; then
  echo "❌ Kör inte som root. Avslutar."
  exit 1
fi

# Installera beroenden
echo "📦 Installing system packages..."
sudo apt update
sudo apt install -y python3-full python3-venv python3-pip sqlite3 git

# Skapa virtuellt Python-miljö
echo "🐍 Creating virtual environment..."
python3 -m venv cigarr-venv
source cigarr-venv/bin/activate

# Installera Python-paket
echo "📦 Installing Python packages..."
pip install plotly

# Initiera databasen
echo "🗄️ Setting up database..."
python3 cigarr_db_setup.py
python3 import_quotes.py

# Skapa första loggningen och HTML
echo "📈 Logging initial data and generating site..."
python3 log_cigarr.py
python3 generate_html.py

echo "✅ Setup complete!"
echo "🔁 You can now run ./update.sh to log and push updates."
