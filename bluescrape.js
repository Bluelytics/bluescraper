// Initialization
var casper = require('casper').create({
    pageSettings: {
        loadImages:  false,        // We don't need images
        loadPlugins: false
    },
    onResourceRequested: function (casp, request, net) {
      if (request.url != 'http://www.dolarblue.net/')
        net.abort();
    }
  });
var utils = require('utils');
var fs = require('fs');
var img;

//This function is our main, where we scrape the data
casper.start("http://www.dolarblue.net/", function() {
  img = this.getElementAttribute('div > img[src^="http://dolarblue"]', 'src')
  fs.write('filename.txt', img, 'w');
});


casper.run();