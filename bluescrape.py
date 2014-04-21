from subprocess import call
import json

call(["casperjs", "dolarbluenet.js"])

with open("dolarbluenet.json", 'rb') as f:
  values = json.loads(f.read())
print values

call(["../bluelytics/add_blue.sh", values['compra'], values['venta'], 'dolarblue.net'])
