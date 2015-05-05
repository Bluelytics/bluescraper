// Initialization
var rURL = 'https://docs.google.com/spreadsheets/d/13hVtAc5ih80ctXT9m28mLPr7oUUNqDGmMUH31eQ2Zw0/pub?output=html';

var casper = require('casper').create({
    verbose: true,
    logLevel: "debug",
    pageSettings: {
        loadImages:  false,        // We don't need images
        loadPlugins: false
    }
  });

  casper.on('remote.message', function(msg) {
      this.echo('remote message caught: ' + msg);
  })
var utils = require('utils');
var fs = require('fs');

//This function is our main, where we scrape the data
casper.start(rURL, function() {
  var out = this.evaluate(function() {
      var rows = document.querySelectorAll('tr');
      var defs = rows[1].querySelectorAll('td');
      var values = rows[2].querySelectorAll('td');

      var compra;
      var venta;
      for(var i = 0; i < defs.length; i++){
        if(defs[i].innerText == "COMPRA"){
	  compra = values[i].innerText.replace(',','.');
	}else if (defs[i].innerText == "VENTA"){
	  venta = values[i].innerText.replace(',','.');
        }
      }
      console.log(venta);
      return {'compra': compra, 'venta': venta};
  });

  fs.write('dolarbluenet.json', JSON.stringify(out), 'w');
});


casper.run();
