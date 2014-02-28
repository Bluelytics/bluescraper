from subprocess import call
import json

with open (".apikey", "r") as apifile:
    api_key= apifile.read().replace('\n','')

import requests
r = requests.get('https://openexchangerates.org/api/latest.json?app_id=' + api_key)
currencies_values = r.json()['rates']

for k in currencies_values.keys():
    cur = currencies_values[k]
    call(["../bluelytics/add_currencyvalue.sh", k, str(cur)])