// Initialization
var rURL = 'http://www.ambito.com/economia/mercados/monedas/dolar/info/?ric=ARSB=';

var casper = require('casper').create({
    pageSettings: {
        loadImages:  false,        // We don't need images
        loadPlugins: false
    },
    onResourceRequested: function (casp, request, net) {
      if (request.url != rURL)
        net.abort();
    }
  });
var utils = require('utils');
var fs = require('fs');

//This function is our main, where we scrape the data
casper.start(rURL, function() {
  var dolarVenta = this.getHTML('div.data-row.sale > span.data-value > strong');
  var dolarCompra = this.getHTML('div.data-row.buy > span.data-value');

  var out = {'venta': dolarVenta.replace(',', '.'), 'compra': dolarCompra.replace(',', '.')};

  fs.write('ambito_out.json', JSON.stringify(out), 'w');
});


casper.run();
