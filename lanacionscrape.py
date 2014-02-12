from subprocess import call
import json

call(["casperjs", "lanacionscrape.js"])

with open("lanacion_out.json", 'rb') as f:
  values = json.loads(f.read())
print values

call(["../bluelytics/add_blue.sh", values['compra'], values['venta'], 'la_nacion'])
