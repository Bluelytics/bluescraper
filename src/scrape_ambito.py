import json, requests, datetime, os
from database import insertBlue

now = datetime.datetime.today()
if now.weekday() < 5 and now.hour >= 10 and now.hour < 23 or 'RUN_ALWAYS' in os.environ:
    r = requests.get('https://mercados.ambito.com/dolar/informal/variacion',
        headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        })
    data = r.json()


    insertBlue('ambito_financiero', data['compra'].replace(',', '.'), data['venta'].replace(',', '.'))
