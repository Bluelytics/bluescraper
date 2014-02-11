#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd $DIR
. $DIR/bin/activate
python $DIR/bluescrape.py
