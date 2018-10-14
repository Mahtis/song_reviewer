from flask import Flask, send_from_directory
from flask_cors import CORS
import subprocess

app = Flask(__name__)
CORS(app)

@app.route("/api/hello")
def hello():
  return "Hello World!"

@app.route("/api/ping")
def ping():
  print('executing')
  subprocess.call('./script.sh', shell=True)
  print('called it')
  return "pong"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('./build/', 'index.html')

if __name__ == '__main__':
    app.run("0.0.0.0", port=8000, debug=True)