from flask import Flask, jsonify, render_template

import subprocess

app = Flask(__name__)

# debug hax
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/api/trigger', methods=("POST",))
def trigger():
    output = subprocess.check_output('./update_lamp.sh')
    return output

@app.route('/')
def index():
    return render_template('index.html')
