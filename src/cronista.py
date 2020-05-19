import json, requests
from bs4 import BeautifulSoup
from database import insertBlue

r = requests.get('https://www.cronista.com/MercadosOnline/dolar.html')

soup = BeautifulSoup(r.text, 'html.parser')


value_buy = float(soup.find(id='dcompra1').get_text().replace('$', '').replace(' ', '').replace(',','.'))
value_sell = float(soup.find(id='dventa1').get_text().replace('$', '').replace(' ', '').replace(',','.'))

if value_buy > 0 and value_sell > 0:
    insertBlue('cronista', value_buy, value_sell)
