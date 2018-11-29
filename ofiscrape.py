from subprocess import call
import json
import requests

r = requests.get('https://mercados.ambito.com/dolar/oficial/variacion')
data = r.json()

call(["../bluelytics/add_blue.sh", data['compra'].replace(',', '.'), data['venta'].replace(',', '.'), 'oficial'])
