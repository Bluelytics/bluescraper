import json, requests
from database import insertBlue

r = requests.get('https://mercados.ambito.com/dolar/oficial/variacion')
data = r.json()

insertBlue('oficial', data['compra'].replace(',', '.'), data['venta'].replace(',', '.'))
