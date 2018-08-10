#!/bin/sh
set -eu
# Called by git post receive hook

# Create environment
rm -rf venv/
python3 -m venv venv
venv/bin/pip install -r requirements.txt
