import json, os, requests
from database import insertCurrencyValue

api_key = os.environ['OPENEX_API_KEY']

import requests
r = requests.get('https://openexchangerates.org/api/latest.json?app_id=' + api_key)
currencies_values = r.json()['rates']

for k in currencies_values.keys():
    cur = currencies_values[k]
    insertCurrencyValue(k, cur)