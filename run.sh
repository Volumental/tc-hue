#!/bin/bash
source venv/bin/activate
FLASK_APP=server.py flask run --host=0.0.0.0 $@
