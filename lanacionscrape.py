from subprocess import call
import json, requests

r = requests.get('https://api-contenidos.lanacion.com.ar/json/V3/economia/cotizacionblue/DBLUE')

if r:
    data = r.json()
    call(["../bluelytics/add_blue.sh", data['compra'].replace(',', '.'), data['venta'].replace(',', '.'), 'invertir_online'])
