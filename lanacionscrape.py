from subprocess import call
import json, requests

r = requests.get('https://api-contenidos.lanacion.com.ar/json/V3/economia/cotizacionblue/DBLUE')

if r:
    data = r.json()
    call(["../bluelytics/add_blue.sh", data['compra'], data['venta'], 'invertir_online'])
