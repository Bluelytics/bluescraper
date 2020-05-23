#!/bin/sh

# Scrape
python scrape_ambito.py
python scrape_lanacion.py
python scrape_oficial.py
python scrape_cronista.py

# Refresh last dolar
python refresh_dolar.py

# Alerts/Updates
python alerts.py
python updates.py
python weekly.py