import json, requests, datetime, os
from lxml import etree
from database import insertBlue

now = datetime.datetime.today()
if now.weekday() < 5 and now.hour >= 10 and now.hour < 23 or 'RUN_ALWAYS' in os.environ:
    r = requests.get('https://www.lanacion.com.ar/tema/dolar-blue-tid67294/',
        headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        })
    tree = etree.HTML(r.text.encode())
    dollar_elems = tree.xpath("//ul[contains(@class, 'dolar-subgroup')]/li/div[contains(@class, 'currency-data')]/p/strong")
    
    buy_value = "".join(dollar_elems[2].itertext()).replace('$', '').replace(',00', '').replace('.','').replace(',','.')
    sell_value = "".join(dollar_elems[3].itertext()).replace('$', '').replace(',00', '').replace('.','').replace(',','.')
    
    insertBlue('lanacion', buy_value, sell_value)
