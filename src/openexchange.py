import json, os, requests
from database import insertNewCurrency

r = requests.get('https://openexchangerates.org/api/currencies.json')
currencies = r.json()

for k in currencies.keys():
    cur = currencies[k]
    insertNewCurrency(k,cur)