// Initialization
var rURL = 'https://docs.google.com/spreadsheet/pub?key=0AtVv0u3p3Ex7dDZaVno5Uno3bWJ0UERpa0hDeDB4eHc&output=html';

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
  var out = this.evaluate(function() {
      var rows = document.querySelectorAll('tr[dir=ltr]');
      var defs = rows[0].querySelectorAll('td');
      var values = rows[1].querySelectorAll('td');
      var compra;
      var venta;
      for(var i = 0; i < defs.length; i++){
        if(defs[i].innerText == "COMPRA"){
	  compra = values[i].innerText.replace(',','.');
	}else if (defs[i].innerText == "VENTA"){
	  venta = values[i].innerText.replace(',','.');
        }
      }
      return {'compra': compra, 'venta': venta};
  });

  fs.write('dolarbluenet.json', JSON.stringify(out), 'w');
});


casper.run();
