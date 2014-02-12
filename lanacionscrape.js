// Initialization
var rURL = 'http://www.lanacion.com.ar/dolar-hoy-t1369';

var casper = require('casper').create({
    pageSettings: {
        loadImages:  false,        // We don't need images
        loadPlugins: false
    }
  });
var utils = require('utils');
var fs = require('fs');

//This function is our main, where we scrape the data
casper.start(rURL, function() {
  var dolarVenta = this.evaluate(function() {
      return document.querySelector('p#bventa').innerText.replace(',','.');
  });
  var dolarCompra = this.evaluate(function() {
      return document.querySelector('p#bcompra').innerText.replace(',','.');
  });

  var out = {'venta': dolarVenta, 'compra': dolarCompra};

  fs.write('lanacion_out.json', JSON.stringify(out), 'w');
});


casper.run();