from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import subprocess
import os
import os.path
import json
from dotenv import load_dotenv
from data_wrangle.model_testing import ReviewModel
import essentia
import essentia.standard as es

app = Flask(__name__)
CORS(app)
load_dotenv()
model = ReviewModel()

@app.route("/api/ping")
def ping():
  return "pong"

@app.route('/api/upload', methods=['POST'])
def upload():
  file = request.files['song']
  file.save('./temp.wav')
  features, features_frames = es.MusicExtractor(lowlevelStats=['mean'],
                                              rhythmStats=['mean'],
                                              tonalStats=['mean'])('./temp.wav')
  row = []
  row.append(features['lowlevel.spectral_complexity.mean'])
  row.append(features['lowlevel.average_loudness'])
  row.append(features['lowlevel.dissonance.mean'])
  row.append(features['lowlevel.pitch_salience.mean'])
  row.append(features['tonal.tuning_frequency'])
  row.append(features['tonal.chords_strength.mean'])
  row.append(features['rhythm.bpm'])
  row.append(features['rhythm.danceability'])
  row.append(features['rhythm.beats_count'])
  row.append(features['metadata.audio_properties.length'])
  row.extend(map_key(features['tonal.chords_key']))
  score = model.predict(row)
  data = {
    'spectral_complexity': features['lowlevel.spectral_complexity.mean'],
    'average_loudness': features['lowlevel.average_loudness'],
    'dissonance': features['lowlevel.dissonance.mean'],
    'pitch_salience': features['lowlevel.pitch_salience.mean'],
    'tuning_frequency': features['tonal.tuning_frequency'],
    'chords_strength': features['tonal.chords_strength.mean'],
    'bpm': features['rhythm.bpm'],
    'danceability': features['rhythm.danceability'],
    'beats_count': features['rhythm.beats_count'],
    'length': features['metadata.audio_properties.length'],
    'chords_key': features['tonal.chords_key'],
    'score': int(score[0])
  }
  # data['score'] = int(score[0])
  return jsonify(data)

# @app.route("/api/json")
# def get_json():
#   print('executing')
#   with open('test.json') as data_file:    
#     data = json.load(data_file)
#   print(data['lowlevel']['average_loudness'])
#   row = []
#   row.append(data['lowlevel']['spectral_complexity']['mean'])
#   row.append(data['lowlevel']['average_loudness'])
#   row.append(data['lowlevel']['dissonance']['mean'])
#   row.append(data['lowlevel']['pitch_salience']['mean'])
#   row.append(data['tonal']['tuning_frequency'])
#   row.append(data['tonal']['chords_strength']['mean'])
#   row.append(data['rhythm']['bpm'])
#   row.append(data['rhythm']['danceability'])
#   row.append(data['rhythm']['beats_count'])
#   row.append(data['metadata']['audio_properties']['length'])
#   row.extend(map_key(data['tonal']['chords_key']))
#   #j = json.load('test.json')
#   # subprocess.call('./script.sh', shell=True)
#   print(row)
#   print('called it')
#   score = model.predict(row)
#   print(score[0])
#   data['score'] = int(score[0])
#   return jsonify(data)

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
  if key in keys:
    return keys[key]
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