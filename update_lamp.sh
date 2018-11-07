#!/bin/sh
cd ${0%/*}
python3 update_lamp.py >stdout 2>stderr
