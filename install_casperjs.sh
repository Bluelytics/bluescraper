#!/bin/bash

wget https://github.com/n1k0/casperjs/zipball/1.1-beta3
mv 1.1-beta3 casperjs.zip
unzip casperjs.zip
rm casperjs.zip
mv n1k0-casperjs-4f105a9 casperjs
ln -s ../casperjs/bin/casperjs bin/casperjs
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.7-linux-x86_64.tar.bz2
tar xfjv phantomjs-1.9.7-linux-x86_64.tar.bz2
mv phantomjs-1.9.7-linux-x86_64 phantomjs
ln -s ../phantomjs/bin/phantomjs bin/phantomjs
rm phantomjs-1.9.7-linux-x86_64.tar.bz2