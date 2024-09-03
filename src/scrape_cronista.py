import json, requests, datetime, os
from lxml import etree
from database import insertBlue

now = datetime.datetime.today()
if now.weekday() < 5 and now.hour >= 10 and now.hour < 23 or 'RUN_ALWAYS' in os.environ:
    r = requests.get('https://www.cronista.com/MercadosOnline/moneda.html?id=ARSB',
        headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        })
    tree = etree.HTML(r.text.encode())
    buy_elem = tree.xpath("//span[contains(@class, 'buy')]/div[contains(@class, 'val')]")[0]
    buy_value = float("".join(buy_elem.itertext()).replace('$', '').replace(',00', '').replace('.',''))
    sell_elem = tree.xpath("//span[contains(@class, 'sell')]/div[contains(@class, 'val')]")[0]
    sell_value = float("".join(sell_elem.itertext()).replace('$', '').replace(',00', '').replace('.',''))

    insertBlue('cronista', buy_value, sell_value)
