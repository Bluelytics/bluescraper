import json, requests, datetime, os
from database import insertBlue

now = datetime.datetime.today()
if now.weekday() < 5 and now.hour >= 10 and now.hour < 23 or 'RUN_ALWAYS' in os.environ:
    r = requests.get('https://www.cronista.com/MercadosOnline/json/eccheader.json')
    data = r.json()


    insertBlue('cronista', data['dolarblue']['valorcompra'], data['dolarblue']['valorventa'])
