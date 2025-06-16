# setup.sh
#!/bin/bash

echo "🔧 Starting setup..."

# Kontrollera att vi kör som rätt användare
if [ "$EUID" -eq 0 ]; then
  echo "❌ Don't run as root. Exiting."
  exit 1
fi

# Install dependencies
echo "📦 Installing system packages..."
sudo apt update
sudo apt install -y python3-full python3-venv python3-pip sqlite3 git

# Create virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv cigarr-venv
source cigarr-venv/bin/activate

# Install Python packages
echo "📦 Installing Python packages..."
pip install plotly

# Initialize database
echo "🗒️ Setting up database..."
python3 cigarr_db_setup.py
python3 import_quotes.py

# Initial log and HTML generation
echo "📈 Logging initial data and generating site..."
python3 log_cigarr.py
python3 generate_html.py

echo "✅ Setup complete!"
echo "🤁 You can now run ./update.sh to log and push updates."
