from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import subprocess
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)
load_dotenv()

if os.getenv('ENV') == 'production':
  # import to use the python library
  print('hallo')
else:
  print('hello')
  # import to use the docker container

@app.route("/api/hello")
def hello():
  print(os.getenv('HELLO'))
  return 'hello'

@app.route("/api/ping")
def ping():
  print('executing')
  subprocess.call('./script.sh', shell=True)
  print('called it')
  return "pong"

@app.route("/api/json")
def get_json():
  print('executing')
  with open('test.json') as data_file:    
    data = json.load(data_file)
  
  #j = json.load('test.json')
  # subprocess.call('./script.sh', shell=True)
  print('called it')
  return jsonify(data)


"""
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('./build/', 'index.html')
"""
if __name__ == '__main__':
    app.run("0.0.0.0", port=8000, debug=True)