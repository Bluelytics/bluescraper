import json, requests, datetime, os
from database import insertBlue

now = datetime.datetime.today()
if now.weekday() < 5 and now.hour >= 10 and now.hour < 23 or 'RUN_ALWAYS' in os.environ:
    r = requests.get('https://api-contenidos.lanacion.com.ar/json/V3/economia/cotizacionblue/DBLUE')

    if r:
        data = r.json()
        insertBlue('invertir_online', data['compra'].replace(',', '.'), data['venta'].replace(',', '.'))