from subprocess import call
import json
import requests

r = requests.get('https://mercados.ambito.com/dolar/informal/variacion')
data = r.json()

call(["../bluelytics/add_blue.sh", data['compra'], data['venta'], 'ambito_financiero'])
