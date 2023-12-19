import stua, export
import json, multiprocessing
from flask import Flask, jsonify
from flask_cors import CORS


VAR = True
DATA = True
LIRR = True
REFRESH = True
DELAY = True

app = Flask(__name__)
CORS(app)

@app.route('/')
def refresh():
    return jsonify(data=export.refresh())


@app.route('/delay')
def delay():
    return jsonify(stua.alertsSubway(planned=False))

@app.route('/lirr')
def lirr():
    with open("lirr.txt", "r") as f:
       return jsonify(data=json.loads(f.read()))

@app.route('/data')
def data():
    with open("data.txt", "r") as f:
       return jsonify(data=json.loads(f.read()))

if __name__ in "__main__":
    multiprocessing.freeze_support()
    app.run(port=7082)