from subprocess import call
import json

import requests
r = requests.get('https://openexchangerates.org/api/currencies.json')
currencies = r.json()

for k in currencies.keys():
    cur = currencies[k]
    call(["../bluelytics/upsert_currencycode.sh", k, cur])
