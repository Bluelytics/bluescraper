import json, requests
from database import insertBlue

r = requests.get('https://mercados.ambito.com/dolar/informal/variacion')
data = r.json()


insertBlue('ambito_financiero', data['compra'].replace(',', '.'), data['venta'].replace(',', '.'))
