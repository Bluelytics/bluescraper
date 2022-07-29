#!/bin/sh

echo "Running scrapers..."
# Scrape
python scrape_ambito.py
python scrape_lanacion.py
python scrape_oficial.py
python scrape_cronista.py

echo "Refreshing dollar..."
# Refresh last dolar
python refresh_dolar.py

echo "Posting updates..."
# Alerts/Updates
python alerts.py
python updates.py
python weekly.py