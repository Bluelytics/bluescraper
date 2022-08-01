import json, requests, datetime, os
from lxml import etree
from database import insertBlue

now = datetime.datetime.today()
if now.weekday() < 5 and now.hour >= 10 and now.hour < 23 or 'RUN_ALWAYS' in os.environ:
    r = requests.get('https://www.cronista.com/MercadosOnline/moneda.html?id=ARSB')
    tree = etree.HTML(r.text)
    buy_elem = tree.xpath("//div[contains(@class, 'buy-value')]")[0]
    buy_value = float("".join(buy_elem.itertext()).replace('$', '').replace(',', '.'))
    sell_elem = tree.xpath("//div[contains(@class, 'sell-value')]")[0]
    sell_value = float("".join(sell_elem.itertext()).replace('$', '').replace(',', '.'))

    insertBlue('cronista', buy_value, sell_value)
