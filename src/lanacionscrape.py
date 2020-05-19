import json, requests
from database import insertBlue

r = requests.get('https://api-contenidos.lanacion.com.ar/json/V3/economia/cotizacionblue/DBLUE')

if r:
    data = r.json()
    insertBlue('invertir_online', data['compra'].replace(',', '.'), data['venta'].replace(',', '.'))