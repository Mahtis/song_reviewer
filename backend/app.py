from flask import Flask
from flask_cors import CORS
app = Flask(__name__)

CORS(app)

@app.route("/")
def hello():
    return "Hello World! pupup"

@app.route("/api/ping")
def ping():
  return "pong"