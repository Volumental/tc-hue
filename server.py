import subprocess

from flask import Flask, jsonify, render_template

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
    output = subprocess.check_output('./update_lamp.sh')
    return output


@app.route('/')
def index():
    latest = {
        'stdout': _slurp('stdout') or '',
        'stderr': _slurp('stderr') or '',
    }
    return render_template('index.html',
        latest=latest,
        config=_slurp('config.json') or 'No config file!')
