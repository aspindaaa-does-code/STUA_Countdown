"""
Ravindra Mangar
Last Updated: 2023-12-19
Project: STUA Countdown Board

main_api.py
----------------------------------------
This file runs the API for the STUA Countdown Board, allowing for the data to be accessed by the web app.
----------------------------------------
"""

# Imports
import stua, export
import json, multiprocessing
from flask import Flask, jsonify
from flask_cors import CORS

# Creates the Flask app and enables CORS.
app = Flask(__name__)
CORS(app)

# Creates the default landing page for the API
@app.route('/')
def refresh():
    return jsonify(data=export.refresh())

# Creates the delays page for the API, returning subway delays from stua.py
@app.route('/delay')
def delay():
    return jsonify(stua.alertsSubway(planned=False))

# Creates the LIRR realtime page for the API, returning LIRR realtime data from export.py
@app.route('/lirr')
def lirr():
    with open("lirr.txt", "r") as f:
       return jsonify(data=json.loads(f.read()))

# Creates the subway/bus realtime page for the API, returning subway/bus realtime data from export.py
@app.route('/data')
def data():
    with open("data.txt", "r") as f:
       return jsonify(data=json.loads(f.read()))

# Enables freezing of the multiprocessing module, to allow for multiprocessing to work on Windows.
# Runs the STUA Countdown Board API on port 7082.
if __name__ in "__main__":
    multiprocessing.freeze_support()
    app.run(host='0.0.0.0', port=7082)