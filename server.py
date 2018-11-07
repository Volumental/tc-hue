import json
import subprocess

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def _slurp(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return None


@app.route('/api/trigger', methods=("POST",))
def trigger():
    subprocess.check_call('./update_lamp.sh')
    return "OK"


@app.route('/api/config', methods=("GET",))
def get_config():
    return _slurp('config.json')


@app.route('/api/config', methods=("POST",))
def post_config():
    with open('config.json', 'w') as f:
        f.write(request.json)
    return "OK"


@app.route('/')
def index():
    latest = {
        'stdout': _slurp('stdout') or '',
        'stderr': _slurp('stderr') or '',
    }
    return render_template('index.html',
        latest=latest,
        config=_slurp('config.json') or 'No config file!')
