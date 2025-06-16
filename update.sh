#!/bin/bash

# Gå till projektkatalog
cd /home/nikke/cigarrprojekt || exit 1

# Aktivera venv
source /home/nikke/cigarr-venv/bin/activate

# Kör skripten
echo "🕒 $(date --iso-8601=seconds)"
python3 log_cigarr.py
python3 generate_statistics.py
python3 generate_stats_json.py
python3 generate_html.py

# Lägg till, committa och pusha
git add docs/index.html docs/stats.html docs/stats_data.json cigarrdata.db
git commit -m "Auto update $(date --iso-8601=seconds)"
git push
