from subprocess import call
import json

call(["casperjs", "elcronistascrape.js"])

with open("elcronista.json", 'rb') as f:
  values = json.loads(f.read())

call(["../bluelytics/add_blue.sh", str(values['compra']), str(values['venta']), 'elcronista'])
