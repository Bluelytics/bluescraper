from subprocess import call
import json

call(["casperjs", "ofiscrape.js"])

with open("oficial_out.json", 'rb') as f:
  values = json.loads(f.read())


call(["../bluelytics/add_blue.sh", values['compra'], values['venta'], 'oficial'])
