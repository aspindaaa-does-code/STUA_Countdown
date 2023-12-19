"""
Ravindra Mangar
Last Updated: 2023-12-19
Project: STUA Countdown Board

main_web.py
----------------------------------------
This file runs the web app for the STUA Countdown Board. The web app downloads data from the API being run on port 7082, in main_api.py.
----------------------------------------
"""

# Imports
from flask import Flask, render_template

# Creates the Flask app.
app = Flask(__name__)

# Creates the default landing page for the web app, whose code in found in /templates/board_final.html.
@app.route("/")
def serve():
    return render_template("board_final.html")

# Runs the STUA Countdown Board web app on port 8082.
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8082)