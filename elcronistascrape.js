// Initialization
var rURL = 'http://mercado.cronista.com:8080/MercadosWeb/home/getPrincipal?jsoncallback=queryDolar';

var casper = require('casper').create({
    pageSettings: {
        loadImages:  false,        // We don't need images
        loadPlugins: false
    }
    
  });
var utils = require('utils');
var fs = require('fs');


casper.start().then(function() {
    this.open(rURL, {
        method: 'get',
        headers: {
            'Accept': 'application/x-javascript'
        }
    });
});

casper.run(function() {
    var dolarJSONP = this.getPageContent();

    var dolarJSON = dolarJSONP.substr(dolarJSONP.indexOf('(')+1, dolarJSONP.lastIndexOf(')')-dolarJSONP.indexOf('(')-1)
    

    var procesado = JSON.parse(dolarJSON);

    for(var i = 0; i < procesado.monedas.length; i++){
      var monedaAct = procesado.monedas[i];
      if (monedaAct.UrlId === "ARSB"){
        var out = {'venta': monedaAct.Venta, 'compra': monedaAct.Compra};
        fs.write('elcronista.json', JSON.stringify(out), 'w');
      }
    }

    this.exit();
});
