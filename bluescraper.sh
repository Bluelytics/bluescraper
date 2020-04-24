#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR
. $DIR/bin/activate
python $DIR/ambitoscrape.py
python $DIR/lanacionscrape.py
python $DIR/ofiscrape.py
