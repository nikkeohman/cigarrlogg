#!/bin/bash
source ~/cigarr-venv/bin/activate
python3 log_cigarr.py
python3 generate_statistics.py
python3 generate_stats_json.py
python3 generate_html.py
git add docs/index.html cigarrdata.db
git commit -m "Auto update $(date +'%Y-%m-%d %H:%M:%S')"
git push

