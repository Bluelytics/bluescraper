import json, requests, datetime, os
from database import insertBlue

now = datetime.datetime.today()
if now.weekday() < 5 and now.hour >= 10 and now.hour < 23 or 'RUN_ALWAYS' in os.environ:
    r = requests.get('https://mercados.ambito.com/dolar/oficial/variacion')
    data = r.json()

    insertBlue('oficial', data['compra'].replace(',', '.'), data['venta'].replace(',', '.'))
