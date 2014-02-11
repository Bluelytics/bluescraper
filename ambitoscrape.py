from subprocess import call
import json

call(["casperjs", "ambitoscrape.js"])

with open("ambito_out.json", 'rb') as f:
  values = json.loads(f.read())

call(["../bluelytics/add_blue.sh", values['compra'], values['venta'], 'ambito_financiero'])
