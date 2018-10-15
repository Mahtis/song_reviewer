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
  print(data['lowlevel']['average_loudness'])
  row = []
  row.append(data['lowlevel']['spectral_complexity']['mean'])
  row.append(data['lowlevel']['average_loudness'])
  row.append(data['lowlevel']['dissonance']['mean'])
  row.append(data['lowlevel']['pitch_salience']['mean'])
  row.append(data['tonal']['tuning_frequency'])
  row.append(data['tonal']['chords_strength']['mean'])
  row.append(data['rhythm']['bpm'])
  row.append(data['rhythm']['danceability'])
  row.append(data['rhythm']['beats_count'])
  row.append(data['metadata']['audio_properties']['length'])
  row.append(data['tonal']['chords_key'])
 
  #j = json.load('test.json')
  # subprocess.call('./script.sh', shell=True)
  print('called it')
  return jsonify(data)

def map_key(key):
  # A#, C, D, D#, E, F#, G, G# 
  keys = {
    'A#': [1, 0, 0, 0, 0, 0, 0, 0],
    'C': [0, 1, 0, 0, 0, 0, 0, 0],
    'D': [0, 0, 1, 0, 0, 0, 0, 0],
    'D#': [0, 0, 0, 1, 0, 0, 0, 0],
    'E': [0, 0, 0, 0, 1, 0, 0, 0],
    'F#': [0, 0, 0, 0, 0, 1, 0, 0],
    'G': [0, 0, 0, 0, 0, 0, 1, 0],
    'G#': [0, 0, 0, 0, 0, 0, 0, 1]
  }
  if keys(key):
    return keys(key)
  else:
    return [0, 0, 0, 0, 0, 0, 0, 0]

"""
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('./build/', 'index.html')
"""
if __name__ == '__main__':
    app.run("0.0.0.0", port=8000, debug=True)