from subprocess import call
import json

#call(["casperjs", "ambitoscrape.js"])

with open("ambito_out.json", 'rb') as f:
  values = json.loads(f.read())

print values['compra']
print values['venta']

#print " ".join(["../bluelytics/add_blue.sh", valorCompra, valorVenta])
#call(["../bluelytics/add_blue.sh", valorCompra, valorVenta])
